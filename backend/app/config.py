from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./medaudit.db"
    REDIS_URL: str = "redis://localhost:6379"
    CLAUDE_API_KEY: str
    OPENAI_API_KEY: str
    SECRET_KEY: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: List[str] = ["http://localhost:5173"]
    STORAGE_PATH: str = "/tmp/medaudit/uploads"

    class Config:
        env_file = ".env"

settings = Settings()
