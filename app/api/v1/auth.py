from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import UserCreate
from app.schemas.auth import LoginRequest, Token
from app.schemas.user import UserResponse, UserCreate
from app.services.auth_services import AuthService
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Start session and get token"""
    service = AuthService(db)

    user = await service.authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = service.create_token_for_user(user)

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Obtain information from the authenticated user"""
    return current_user

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_first_admin(
        user_data: UserCreate,
        db: AsyncSession = Depends(get_db)):
    """Registro publico, solo funciona si no hay usuarios en el sistema. El primer usuario siempre sera ADMIN"""
    service = UserService(db)
    total = await service.count_users()
    if total > 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ya existe usuarios. Use /auth/login y luego /users/ para crear mas."
        )

    #Forzar rol admin para el primer usuario
    user_data_dict = user_data.model_dump()
    user_data_dict["role"] = "admin"
    first_admin = UserCreate(**user_data_dict)

    try:
        user = await service.create_user(first_admin)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = str(e)
        )