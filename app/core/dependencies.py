from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.database import get_db
from app.models import UserRole
from app.models.user import User
from app.repositories.user_repository import UserRepository

# Esquema de seguridad Bearer
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),
                           db: AsyncSession = Depends(get_db)) -> User:
    """Obtain current user"""
    """Obtiene el usuario actual a partir del token JWT"""
    token = credentials.credentials
    payload = decode_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found invalid/expired",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid",
            headers={"WWW-Authenticate": "Bearer"}
        )

    repository = UserRepository(db)
    user = await repository.get_by_id(int(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user

#Proteger endpoints
def require_roles(allowed_roles: list[UserRole]):
    """Crea una dependencia que verifica si el usuario tiene uno de los roles"""
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere uno de estos roles: {[r.value for r in allowed_roles]}"
            )
        return current_user
    return role_checker

#Dependencias predefinidas por rol
require_admin = require_roles([UserRole.ADMIN])
require_admin_or_contador = require_roles([UserRole.ADMIN, UserRole.CONTADOR])

