from decimal import Decimal

from pydantic import Field

from app.models.persona import TipoPersona, TipoIdentificacion, TipoContacto
from app.schemas.base import BaseSchema, BaseResponseSchema

# ══════════════════════════════════════════
# IDENTIFICACIÓN
# ══════════════════════════════════════════
class IdentificacionCreate(BaseSchema):
    """Schema para crear identificacion"""
    tipo: TipoIdentificacion
    numero: str = Field(min_length=5, max_length=30)
    es_principal: bool = False

class IdentificacionResponse(BaseSchema):
    """Schema de respuesta de identificacion"""
    persona_id: int
    tipo: TipoIdentificacion
    numero: str
    es_principal: bool


# ══════════════════════════════════════════
# CONTACTO
# ══════════════════════════════════════════
class ContactoCreate(BaseSchema):
    """Schema para crear contacto"""
    tipo: TipoContacto
    valor: str = Field(min_length=1, max_length=300)
    es_principal: bool = False

class ContactoResponse(BaseSchema):
    """Schema de respuesta de contacto"""
    persona_id: int
    tipo: TipoContacto
    valor: str
    es_principal: bool

# ══════════════════════════════════════════
# PERSONA
# ══════════════════════════════════════════

class PersonaCreate(BaseSchema):
    """schema for create a person"""
    tipo_persona: TipoPersona

    # Natural
    nombre: str | None = Field(default=None, max_length=250)
    apellido: str | None = Field(default=None, max_length=250)

    # Juridica
    razon_social: str | None = Field(default=None, max_length=400)
    nombre_comercial: str | None = Field(default=None, max_length=400)

    # Identificaciones y contactos iniciales
    identificaciones: list[IdentificacionCreate] = []
    contactos: list[ContactoCreate] = []
    #tipo_identificacion: TipoIdentificacion
    #numero_identificacion: str = Field(min_length=8, max_length=30)

    #tipo: TipoPersona
    #direccion: str | None = None
    #telefono: str | None = Field(default=None, max_length=20)
    #email: EmailStr | None = None
    #limite_credito: float = Field(default=0.00, ge=0)
    #dias_credito: int = Field(default=0, ge=0)

class PersonaUpdate(BaseSchema):
    """Schema for update a person"""
    #tipo_identificacion: TipoIdentificacion | None = None
    #numero_identificacion: str | None = Field(default=None, min_length=8, max_length=30)
    #razon_social: str | None = Field(default=None, min_length=2, max_length=400)
    #nombre_comercial: str | None = None
    #tipo: TipoPersona | None = None
    #direccion: str | None = None
    #telefono: str | None = Field(default=None, max_length=20)
    #email: EmailStr | None = None
    #limite_credito: float | None = Field(default=None, ge=0)
    #dias_credito: int | None = Field(default=None, ge=0)
    tipo_persona: TipoPersona | None = None
    nombre: str | None = Field(default=None, max_length=250)
    apellido: str | None = Field(default=None, max_length=250)
    razon_social: str | None = Field(default=None, max_length=400)
    nombre_comercial: str | None = Field(default=None, max_length=400)
    is_active: bool | None = None

# Schema de SALIDA

class PersonaResponse(BaseResponseSchema):
    """Schema for returning a person"""
    #tipo_identificacion: TipoIdentificacion
    #numero_identificacion: str
    #razon_social: str
    #nombre_comercial: str | None
    #tipo: TipoPersona
    #direccion: str | None
    #telefono: str | None
    #email: str | None
    #limite_credito: float
    #dias_credito: int
    tipo_persona: TipoPersona
    nombre: str | None
    apellido: str | None
    razon_social: str | None
    nombre_comercial: str | None
    identificaciones: list[IdentificacionResponse] = []
    contactos: list[ContactoResponse] = []

class PersonaList(BaseSchema):
    """Schema for returning a list of persons"""
    personas: list[PersonaResponse]
    total: int
    page: int
    per_page: int


# ══════════════════════════════════════════
# CLIENTE
# ══════════════════════════════════════════
class ClienteCreate(BaseSchema):
    """schema for create a cliente"""
    persona_id: int
    limite_credito: Decimal = Field(default=Decimal("0"), ge=0)
    dias_credito: int = Field(default=0, ge=0)

class ClienteCreateWithPersona(BaseSchema):
    """schema for create a cliente with new persona"""
    persona: PersonaCreate

    #Datos de cliente
    limite_credito: Decimal = Field(default=Decimal("0"), ge=0)
    dias_credito: int = Field(default=0, ge=0)

class ClienteUpdate(BaseSchema):
    """schema for update a cliente"""
    limite_credito: Decimal = Field(default=Decimal("0"), ge=0)
    dias_credito: int = Field(default=0, ge=0)
    is_active: bool | None = None

class ClienteResponse(BaseSchema):
    """Schema for returning a cliente"""
    persona_id: int
    limite_credito: Decimal
    dias_credito: int
    persona: PersonaResponse

class ClienteList(BaseSchema):
    """schema for returning a list of clientes"""
    clientes: list[ClienteResponse]
    total: int
    page: int
    per_page: int

# ══════════════════════════════════════════
# PROVEEDOR
# ══════════════════════════════════════════

class ProveedorCreate(BaseSchema):
    """Schema para crear proveedor."""
    persona_id: int
    dias_credito: int = Field(default=0, ge=0)
    cuenta_bancaria: str | None = Field(default=None, max_length=50)
    banco: str | None = Field(default=None, max_length=100)


class ProveedorCreateWithPersona(BaseSchema):
    """Schema para crear proveedor con persona nueva."""
    persona: PersonaCreate
    dias_credito: int = Field(default=0, ge=0)
    cuenta_bancaria: str | None = Field(default=None, max_length=50)
    banco: str | None = Field(default=None, max_length=100)


class ProveedorUpdate(BaseSchema):
    """Schema para actualizar proveedor."""
    dias_credito: int | None = Field(default=None, ge=0)
    cuenta_bancaria: str | None = Field(default=None, max_length=50)
    banco: str | None = Field(default=None, max_length=100)
    is_active: bool | None = None


class ProveedorResponse(BaseResponseSchema):
    """Schema de respuesta de proveedor."""
    persona_id: int
    dias_credito: int
    cuenta_bancaria: str | None
    banco: str | None
    persona: PersonaResponse


class ProveedorList(BaseSchema):
    """Schema para listar proveedores."""
    proveedores: list[ProveedorResponse]
    total: int
    page: int
    per_page: int


# ══════════════════════════════════════════
# EMPLEADO
# ══════════════════════════════════════════

class EmpleadoCreate(BaseSchema):
    """Schema para crear empleado."""
    persona_id: int
    cargo: str | None = Field(default=None, max_length=100)
    salario: Decimal = Field(default=Decimal("0"), ge=0)
    fecha_ingreso: str | None = None  # YYYY-MM-DD


class EmpleadoCreateWithPersona(BaseSchema):
    """Schema para crear empleado con persona nueva."""
    persona: PersonaCreate
    cargo: str | None = Field(default=None, max_length=100)
    salario: Decimal = Field(default=Decimal("0"), ge=0)
    fecha_ingreso: str | None = None


class EmpleadoUpdate(BaseSchema):
    """Schema para actualizar empleado."""
    cargo: str | None = Field(default=None, max_length=100)
    salario: Decimal | None = Field(default=None, ge=0)
    fecha_ingreso: str | None = None
    is_active: bool | None = None


class EmpleadoResponse(BaseResponseSchema):
    """Schema de respuesta de empleado."""
    persona_id: int
    cargo: str | None
    salario: Decimal | None
    fecha_ingreso: str | None
    persona: PersonaResponse


class EmpleadoList(BaseSchema):
    """Schema para listar empleados."""
    empleados: list[EmpleadoResponse]
    total: int
    page: int
    per_page: int