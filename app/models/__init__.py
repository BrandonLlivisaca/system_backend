from app.models.base import BaseModel
from app.models.user import User, UserRole
from app.models.persona import (Persona,
                                Identifacion,
                                Contacto,
                                Cliente,
                                Proveedor,
                                Empleado,
                                TipoPersona,
                                TipoIdentificacion,
                                TipoContacto
                                )

__all__ = [
    'BaseModel',
    'User',
    'UserRole',
    'Persona',
    'Identifacion',
    'Contacto',
    'Cliente',
    'Proveedor',
    'Empleado',
    'TipoPersona',
    'TipoIdentificacion',
    'TipoContacto',

]
