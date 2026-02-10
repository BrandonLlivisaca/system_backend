from enum import Enum

from sqlalchemy import String, Numeric, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseModel

class TipoIdentificacion(str, Enum):
    """Identification Type"""
    RUC = "ruc"
    CEDULA = "cedula"
    PASAPORTE = "pasaporte"

class TipoPersona(str, Enum):
    """Type of third parties"""
    CLIENTE = "cliente"
    PROVEEDOR = "proveedor"
    EMPLEADO = "empleado"

class Persona(BaseModel):
    __tablename__ = "persona"

    # Identification
    tipo_identificacion: Mapped[TipoIdentificacion] = mapped_column(
        String(30),
        unique=True,
        index=True,
        nullable=False
    )

    numero_identificacion: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        index=True,
        nullable=False
    )

    # Basic Information
    razon_social: Mapped[str] = mapped_column(String(400), nullable=False)
    nombre_comercial: Mapped[str] = mapped_column(String(400), nullable=False)

    # Tipo de persona
    tipo: Mapped[TipoPersona] = mapped_column(String(30), nullable=False)

    # Contacto
    direccion: Mapped[str | None] = mapped_column(Text, nullable=True)
    telefono: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(200), nullable=True)

    # Datos comerciales
    limite_credito: Mapped[float] = mapped_column(
        Numeric(12,2),
        default=0.00
    )
    dias_credito: Mapped[int] = mapped_column(Integer, default=0)







