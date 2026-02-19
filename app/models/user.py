from enum import Enum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseModel

class UserRole(str, Enum):
    """Roles available in the system"""
    ADMIN = "admin"
    VENDEDOR = "vendedor"
    COMPRADOR = "comprador"
    ALMACENERO = "almacenero"
    CONTADOR = "contador"

class User(BaseModel):
    """User model of system"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        String(20),
        default=UserRole.VENDEDOR,
        nullable=False
    )

