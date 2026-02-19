from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Identificacion
from app.models.persona import Persona, TipoPersona
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
                    Identificacion.is_active == True,
                    Persona.is_active == True
                )
                .options(selectinload(Persona.identificacion))
            )
            result = await self.db.execute(query)
            return result.scalar_one_or_none()

    async def get_by_id(self, id: int) -> Persona | None:
        """Obtiene una persona por ID con sus relaciones."""
        query = (
            select(Persona)
            .where(Persona.id == id, Persona.is_active == True)
            .options(
                selectinload(Persona.identificacion)
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_tipo(self, tipo: TipoPersona, skip: int = 0,
                          limit: int = 100) -> list[Persona] | None:
        """Search a person by tipo"""
        query = select(Persona).where(
            Persona.tipo == tipo,
            Persona.is_active.is_(True)
        ).offset(skip).limit(limit)

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def identificacion_exists(self, numero: str) -> bool:
        """Verify if a identification number exists"""
        persona = await self.get_by_identificacion(numero)
        return persona is not None

class IdentificacionRepository(BaseRepository[Identificacion]):
    """Repository para identificaciones."""
    def __init__(self, db: AsyncSession):
        super().__init__(Identificacion, db)