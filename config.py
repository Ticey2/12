#from pydantic import BaseSettings
from dotenv import load_dotenv
import os
class Settings:
    app_name: str = "New API"
    admin_email: str = "ponOlgap@gmail.com"
    DATABASE_URL: str = "sqlite:///./test02.db"
    POSTGRES_DATABASE_URL: str = "postgresql://user:password@postgresserver/db"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

load_dotenv()
settings = Settings()

settings.POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
settings.POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
settings.POSTGRES_USER = os.environ.get('POSTGRES_USER')
settings.POSTGRES_DB = os.environ.get('POSTGRES_DB')
settings.POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
settings.POSTGRES_DATABASE_URL = f"postgres+asyncpg2:" \
                                 f"//{settings.POSTGRES_USER}:" \
                                 f"{settings.POSTGRES_PASSWORD}" \
                                 f"@{settings.POSTGRES_HOST}:" \
                                 f"{settings.POSTGRES_PORT}" \
                                 f"/{settings.POSTGRES_DB}"
