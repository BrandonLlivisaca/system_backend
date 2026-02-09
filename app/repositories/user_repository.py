from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    """User specific repository"""
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def get_by_email(self, email: str) -> User | None:
        """ Search for a user by mail"""
        query = select(User).where(User.email == email,
                                   User.is_active.is_(True))
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def email_exists(self, email: str) -> bool:
        """Verify if a user exists"""
        user = await self.get_by_email(email)
        return user is not None

