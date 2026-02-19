from enum import Enum

from sqlalchemy import String, Numeric, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel

class TipoIdentificacion(str, Enum):
    """Identification Type"""
    RUC = "ruc"
    CEDULA = "cedula"
    PASAPORTE = "pasaporte"

class TipoPersona(str, Enum):
    """Type of person"""
    NATURAL = "natural"
    JURIDICA = "juridica"

class TipoContacto(str, Enum):
    "Type of contact"
    TELEFONO = "telefono"
    CELULAR = "celular"
    EMAIL = "email"
    DIRECCION = "direccion"

class Persona(BaseModel):
    __tablename__ = "persona"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tipo_persona: Mapped[TipoPersona] = mapped_column(String(20), nullable=False)

    # Identification
    # tipo_identificacion: Mapped[TipoIdentificacion] = mapped_column(
    #     String(30),
    #     unique=True,
    #     index=True,
    #     nullable=False
    # )

    # numero_identificacion: Mapped[str] = mapped_column(
    #     String(30),
    #     unique=True,
    #     index=True,
    #     nullable=False
    # )

    # Basic Information - Natural Person
    nombre: Mapped[str | None] = mapped_column(String(250))
    apellido: Mapped[str | None] = mapped_column(String(250))

    # Basic Information - Juridic Person
    razon_social: Mapped[str | None] = mapped_column(String(400), nullable=True)
    nombre_comercial: Mapped[str | None] = mapped_column(String(400), nullable=True)

    # Tipo de persona
    #tipo: Mapped[TipoPersona] = mapped_column(String(30), nullable=False)

    # Relations
    identificacion: Mapped[list["Identificacion"]] = relationship(
        "Identificacion",
        back_populates="persona",
        cascade="all, delete-orphan",
    )

    contacto: Mapped[list["Contacto"]] = relationship(
        "Contacto",
        back_populates="persona",
        cascade="all, delete-orphan",
    )

    cliente: Mapped["Cliente | None"] = relationship(
        "Cliente",
        back_populates="persona",
        uselist=False,
    )

    proveedor: Mapped["Proveedor | None"] = relationship(
        "Proveedor",
        back_populates="persona",
        uselist=False,
    )

    empleado: Mapped["Empleado | None"] = relationship(
        "Empleado",
        back_populates="persona",
        uselist=False,
    )


    # Contacto
    #direccion: Mapped[str | None] = mapped_column(Text, nullable=True)
    #telefono: Mapped[str | None] = mapped_column(String(20), nullable=True)
    #email: Mapped[str | None] = mapped_column(String(200), nullable=True)

    # Datos comerciales
    #limite_credito: Mapped[float] = mapped_column(
     #   Numeric(12,2),
      #  default=0.00
    #)
    #dias_credito: Mapped[int] = mapped_column(Integer, default=0)

class Identificacion(BaseModel):
    """Identificacion de una persona"""
    __tablename__ = "identificacion"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    persona_id: Mapped[int] = mapped_column(ForeignKey("persona.id"), nullable=False)
    tipo: Mapped[TipoIdentificacion] = mapped_column(String(30), nullable=False)
    numero: Mapped[str] = mapped_column(String(30), nullable=False, unique=True, index=True)
    es_principal: Mapped[bool] = mapped_column(default=False, nullable=False)

    # Relation
    persona: Mapped[Persona] = relationship(
        "Persona",
        back_populates="identificacion"
    )

class Contacto(BaseModel):
    __tablename__ = "contacto"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    persona_id: Mapped[int] = mapped_column(ForeignKey("persona.id"), nullable=False)
    tipo: Mapped[TipoIdentificacion] = mapped_column(String(30), nullable=False)
    valor: Mapped[String] = mapped_column(String(300), nullable=False, unique=True, index=True)

    #Relation
    persona: Mapped[Persona] = relationship(
        "Persona",
        back_populates="contacto"
    )

class Cliente(BaseModel):
    """Information of a client"""
    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    persona_id: Mapped[int] = mapped_column(
        ForeignKey("persona.id"),
        nullable=False,
        unique=True
    )

    limite_credito: Mapped[Numeric] = mapped_column(Numeric(12,2))
    dias_credito: Mapped[Numeric] = mapped_column(Numeric(12,2))

    #Relation
    persona: Mapped[Persona] = relationship(
        "Persona",
        back_populates="cliente"
    )

class Proveedor(BaseModel):
    """Information of a proveedor"""
    __tablename__ = "proveedor"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    persona_id: Mapped[int] = mapped_column(
        ForeignKey("persona.id"),
        unique=True,
        nullable=False
    )

    dias_credito: Mapped[int] = mapped_column(Integer, default=0)
    # la cuenta bancaria debe ser una tabla

    # Relation
    persona: Mapped[Persona] = relationship(
        "Persona",
        back_populates="proveedor"
    )

class Empleado(BaseModel):
    """Information of a employed"""
    __tablename__ = "empleado"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    persona_id: Mapped[int] = mapped_column(
        ForeignKey("persona.id"),
        unique=True,
        nullable=False
    )
    cargo: Mapped[String] = mapped_column(String(150), nullable=True)
    salario: Mapped[Numeric] = mapped_column(Numeric(12,2), default=0)
    #fecha_ingreso: Mapped[String | None] = mapped_column(String, nullable=True)
    fecha_ingreso: Mapped[str | None] = mapped_column(String(10))

    #Relation
    persona: Mapped[Persona] = relationship(
        "Persona",
        back_populates="empleado"
    )








