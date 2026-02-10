from pydantic import EmailStr, Field

from app.models.persona import TipoPersona, TipoIdentificacion
from app.schemas.base import BaseSchema, BaseResponseSchema

# Schemas de entrada

class PersonaCreate(BaseSchema):
    """schema for create a person"""
    tipo_identificacion: TipoIdentificacion
    numero_identificacion: str = Field(min_length=8, max_length=30)
    razon_social: str = Field(min_length=1, max_length=400)
    nombre_comercial: str | None = None
    tipo: TipoPersona
    direccion: str | None = None
    telefono: str | None = Field(default=None, max_length=20)
    email: EmailStr | None = None
    limite_credito: float = Field(default=0.00, ge=0)
    dias_credito: int = Field(default=0, ge=0)

class PersonaUpdate(BaseSchema):
    """Schema for update a person"""
    tipo_identificacion: TipoIdentificacion | None = None
    numero_identificacion: str | None = Field(default=None, min_length=8, max_length=30)
    razon_social: str | None = Field(default=None, min_length=2, max_length=400)
    nombre_comercial: str | None = None
    tipo: TipoPersona | None = None
    direccion: str | None = None
    telefono: str | None = Field(default=None, max_length=20)
    email: EmailStr | None = None
    limite_credito: float | None = Field(default=None, ge=0)
    dias_credito: int | None = Field(default=None, ge=0)
    is_active: bool | None = None

# Schema de SALIDA

class PersonaResponse(BaseResponseSchema):
    """Schema for returning a person"""
    tipo_identificacion: TipoIdentificacion
    numero_identificacion: str
    razon_social: str
    nombre_comercial: str | None
    tipo: TipoPersona
    direccion: str | None
    telefono: str | None
    email: str | None
    limite_credito: float
    dias_credito: int

class PersonaList(BaseSchema):
    """Schema for returning a list of persons"""
    personas: list[PersonaResponse]
    total: int
    page: int
    per_page: int


