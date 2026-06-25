import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:pass@localhost/angel_pocket"
    SECRET_KEY: str = "supersecret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    GRA_INFLUENCE_WEIGHT: float = 0.5
    GRA_MAX_ITER: int = 20
    GRA_EPSILON: float = 1e-4
    GRA_NULLIFICATION_THRESHOLD: float = 0.7
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
