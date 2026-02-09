from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration of the aplication"""

    APP_NAME: str = 'SYSTEM BACKEND'
    DEBUG: bool = True

    #Base de datos
    DATABASE_URL: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    #class Config:
     #   env_file = ".env"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

#Global Configuration Instance
settings = Settings()

