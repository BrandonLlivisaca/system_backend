from app.models.base import BaseModel
from app.models.user import User, UserRole
from app.models.persona import (Persona,
                                Identificacion,
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
    'Identificacion',
    'Contacto',
    'Cliente',
    'Proveedor',
    'Empleado',
    'TipoPersona',
    'TipoIdentificacion',
    'TipoContacto',

]
