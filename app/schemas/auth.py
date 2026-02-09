from pydantic import EmailStr
from app.schemas.base import BaseSchema

class LoginRequest(BaseSchema):
    """Login Schema"""
    email: EmailStr
    password: str

class Token(BaseSchema):
    """Schema para respuesta de token"""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseSchema):
    """Schema para datos dentro del token"""
    user_id: int | None = None
    email: str | None = None
