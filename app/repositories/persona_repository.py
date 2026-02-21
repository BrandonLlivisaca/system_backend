from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Identificacion
from app.models.persona import Persona, TipoPersona, Contacto
from app.repositories.base import BaseRepository

class PersonaRepository(BaseRepository[Persona]):
    """Repository for Person"""
    def __init__(self, db: AsyncSession):
        super().__init__(Persona, db)

    async def get_by_identificacion(self, numero: str) -> Persona | None:
            """Busca una persona por número de identificación."""
            query = (
                select(Persona)
                .join(Identificacion)
                .where(
                    Identificacion.numero == numero,
                    Identificacion.is_active.is_(True),
                    Persona.is_active.is_(True)
                )
                .options(selectinload(Persona.identificacion))
            )
            result = await self.db.execute(query)
            return result.scalar_one_or_none()

    async def get_by_id(self, id: int) -> Persona | None:
        """Obtiene una persona por ID con sus relaciones."""
        query = (
            select(Persona)
            .where(Persona.id == id, Persona.is_active.is_(True))
            .options(
                selectinload(Persona.identificacion)
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_tipo(self, tipo: TipoPersona, skip: int = 0,
                          limit: int = 100) -> list[Persona] | None:
        """Search a person by tipo"""
        query = (select(Persona)
                 .join(Identificacion)
                 .where(
            Identificacion.is_active.is_(True),
                        Persona.tipo_persona==tipo,
                        Persona.is_active.is_(True))
                 .options(selectinload(Persona.identificacion))
                 .offset(skip).limit(limit))

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Persona]:
        """Retrieves all active records with pagination """
        query = (select(Persona)
                 .join(Identificacion)
                 .join(Contacto)
                 .where(Identificacion.is_active.is_(True),
                        Persona.is_active.is_(True),
                        Contacto.is_active.is_(True))
                 .options(selectinload(Persona.identificacion))
                 .options(selectinload(Persona.contacto))
                 .offset(skip).limit(limit))

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count_persons(self):
        query = (select(func.count(Persona.id))
                 .where(Persona.is_active.is_(True)))
        result = await self.db.execute(query)
        return result.scalar() or 0

    async def identificacion_exists(self, numero: str) -> bool:
        """Verify if a identification number exists"""
        persona = await self.get_by_identificacion(numero)
        return persona is not None

class IdentificacionRepository(BaseRepository[Identificacion]):
    """Repository para identificaciones."""
    def __init__(self, db: AsyncSession):
        super().__init__(Identificacion, db)

class ContactoRepository(BaseRepository[Contacto]):
    """Repository para contactos."""
    def __init__(self, db: AsyncSession):
        super().__init__(Contacto, db)