from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password, create_access_token
from app.config import settings
from app.models.user import User
from app.repositories.user_repository import UserRepository

class AuthService:
    """Authentication Service"""
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repository = UserRepository(db)

    async def authenticate_user(self, email: str, password: str) -> User | None:
        """Verify credentials and return user if they are valid"""
        user = await self.user_repository.get_by_email(email)

        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    def create_token_for_user(self, user: User) -> str:
        """Create token JWT for user"""
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role
        }

        expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return create_access_token(data=token_data, expires_delta=expires)