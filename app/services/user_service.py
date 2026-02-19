from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate

class UserService:
    """Service with business logic for users"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = UserRepository(db)

    async def create_user(self, user_data: UserCreate) -> User:
        """Create new user"""
        #Check if the mail already exists
        if await self.repository.email_exists(user_data.email):
            raise ValueError('Email already exists')

        #Prepare data with encrypted password
        user_dict = user_data.model_dump()

        # DEBUG: Ver qué contiene el password
        # print(f"Password recibido: '{user_dict['password']}'")
        # print(f"Longitud: {len(user_dict['password'])}")

        user_dict["hashed_password"] = hash_password(user_dict.pop("password"))

        #Create user
        return await self.repository.create(user_dict)

    async def get_user(self, user_id: int) -> User | None:
        """Getting user by id"""
        return await self.repository.get_by_id(user_id)

    async def get_user_by_email(self, email: str) -> User | None:
        """Getting user by email"""
        return await self.repository.get_by_email(email)

    async def get_users(self, skip: int = 0, limit: int = 100) -> list[User] | None:
        """Getting all users"""
        return await self.repository.get_all(skip=skip, limit=limit)

    async def update_user(self, user_id: int, user_data: UserUpdate) -> User | None:
        """Updating user"""
        user = await self.repository.get_by_id(user_id)
        if not user:
            return None

        #If there is a password, encrypt it
        update_dict = user_data.model_dump(exclude_unset=True)
        if "password" in update_dict:
            update_dict["hashed_password"] = hash_password(update_dict.pop("password"))

        return await self.repository.update(user, update_dict)

    async def delete_user(self, user_id: int) -> User | None:
        """Deleting user"""
        user = await self.repository.get_by_id(user_id)
        if not user:
            return None

        return await self.repository.delete(user)

    async def count_users(self) -> int:
        """Count user"""
        try:
            return await self.repository.count()
        except Exception as e:
            raise ValueError(f'Error counting users: {e}')


