from pydantic import EmailStr, Field

from app.models.user import UserRole
from app.schemas.base import BaseSchema, BaseResponseSchema


# ══════════════════════════════════════════
# Schemas de ENTRADA (lo que recibe la API)
# ══════════════════════════════════════════

class UserCreate(BaseSchema):
    """Schema para crear un usuario."""

    email: EmailStr
    password: str = Field(min_length=6, max_length=100)
    full_name: str = Field(min_length=2, max_length=100)
    role: UserRole = UserRole.VENDEDOR


class UserUpdate(BaseSchema):
    """Schema para actualizar un usuario (todos los campos opcionales)."""

    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=6, max_length=100)
    full_name: str | None = Field(default=None, min_length=2, max_length=100)
    role: UserRole | None = None
    is_active: bool | None = None


# ══════════════════════════════════════════
# Schemas de SALIDA (lo que devuelve la API)
# ══════════════════════════════════════════

class UserResponse(BaseResponseSchema):
    """Schema para devolver un usuario (sin password)."""

    email: str
    full_name: str
    role: UserRole


class UserList(BaseSchema):
    """Schema para listar usuarios con paginación."""

    users: list[UserResponse]
    total: int
    page: int
    per_page: int