from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserList
from app.services.user_service import UserService
from app.models.user import User, UserRole
from app.core.dependencies import get_current_user, require_roles

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate,
                      db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(require_roles([UserRole.ADMIN]))):
    """Create new user."""
    service = UserService(db)

    try:
        user = await service.create_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(e))

@router.get("/", response_model=UserList)
async def get_users(skip: int = 0, limit: int = 10,
                    db: AsyncSession = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    """Get all users."""
    service = UserService(db)

    users = await service.get_users(skip=skip, limit=limit)
    total = await service.count_users()

    return {
        "users": users,
        "total": total,
        "page": (skip // limit) + 1,
        "per_page": limit
    }

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    """Get user for given id."""
    service = UserService(db)
    user = await service.get_user(user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int,
                      user_data: UserUpdate,
                      db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    """Update user. User can editar a si mismo, ADMIN puede editar a todos"""
    #Verificar permisos
    if current_user.id != user_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You can only edit your own profile")

    #Solo ADMIN puede cambiar roles
    if user_data.role is not None and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Solo ADMIN puede cambiar roles")

    service = UserService(db)
    user = await service.update_user(user_id, user_data)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int,
                      db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(require_roles([UserRole.ADMIN]))):
    #Delete user only admin
    if current_user.id == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You can't delete your own profile")

    """Delete user"""
    service = UserService(db)
    user = await service.delete_user(user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    return None
