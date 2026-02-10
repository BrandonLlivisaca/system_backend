from typing import Any, Coroutine

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Persona
from app.models.persona import Persona, TipoPersona
from app.repositories.persona_repository import PersonaRepository
from app.schemas.persona import PersonaCreate, PersonaUpdate

class PersonaService:
    """Service for persona business logic"""
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = PersonaRepository(db)

    async def create_persona(self, data: PersonaCreate) -> ValueError | Persona:
        """Create a new persona"""
        # Verify if the identification number exists
        if await self.repository.identificacion_exists(data.numero_identificacion):
            raise ValueError("Identification number already exists")

        return await self.repository.create(data.model_dump())

    async def get_persona(self, persona_id: int) -> Persona | None:
        """Get a persona for id"""
        return await self.repository.get_by_id(persona_id)

    async def get_persona_by_identification(self, numero: str) -> Persona | None:
        """Get a person for identification number"""
        return await self.repository.get_by_identifacion(numero)

    async def get_person_list(self,
                              skip: int = 0,
                              limit: int = 100,
                              tipo: TipoPersona | None = None) -> list[Persona]:
        """Get a person list"""
        if tipo:
            return await self.repository.get_by_tipo(tipo, skip, limit)

        return await self.repository.get_all(skip, limit)

    async def update_persona(self, persona_id: int, data: PersonaUpdate) -> Persona | None:
        """Update a person"""
        persona = await self.repository.get_by_id(persona_id)
        if not persona:
            return None

        # Si cambia la identificacion, verificar que no exista
        update_data = data.model_dump(exclude_unset=True)
        if "numero_identificacion" in update_data:
            numero_nuevo = update_data["numero_identificacion"]
            if numero_nuevo != persona.numero_identificacion:
                if await self.repository.identificacion_exists(numero_nuevo):
                    raise ValueError("Identification number already exists")

        return await self.repository.update(persona, update_data)

    async def delete_person(self, persona_id: int) -> Persona | None:
        """Delete a person"""
        print("gele")
        persona = await self.repository.get_by_id(persona_id)
        if not persona:
            return None

        return await self.repository.delete(persona)

    async def count_persons(self):
        """Count all persons"""
        return await self.repository.count()

