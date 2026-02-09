from typing import Generic, TypeVar, Type
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """Repository base con operaciones CRUD genericas"""

    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get_by_id(self, id: int) -> ModelType | None:
        """Gets one record by id"""
        query = select(self.model).where(
            self.model.id == id,
            self.model.is_active.is_(True)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelType]:
        """Retrieves all active records with pagination """
        query = select(self.model).where(
            self.model.is_active.is_(True)
        ).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def create(self, obj_data: dict) -> ModelType:
        """Create a new record"""
        db_obj = self.model(**obj_data)
        self.db.add(db_obj)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: ModelType, obj_data: dict) -> ModelType:
        """Update an existing record"""
        for field, value in obj_data.items():
            if value is not None:
                setattr(db_obj, field, value)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, db_obj: ModelType) -> ModelType:
        """Soft delete - marked as inactive"""
        db_obj.is_active = False
        await self.db.flush()
        return db_obj

    # async def count(self) -> int:
    #     """Count active records"""
    #     query = select(func.count()).select(self.model).where(
    #         self.model.is_active.is_(True)
    #     )
    #     #query = select(self.model).where(self.model.is_active.is_(True))
    #     result = await self.db.execute(query)
    #     #return = len(result.scalars().all())
    #     return result.scalar()

    async def count(self) -> int:
        """Cuenta registros activos."""
        # query = select(func.count()).select(self.model).where(self.model.is_active.is_(True))
        # result = await self.db.execute(query)
        # return len(result.scalars().all())
        """Cuenta registros activos."""
        query = select(func.count(self.model.id)).where(self.model.is_active.is_(True))
        result = await self.db.execute(query)
        return result.scalar() or 0
