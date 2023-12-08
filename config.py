#from pydantic import BaseSettings

class Settings:
    app_name: str = "New API"
    admin_email: str = "ponOlgap@gmail.com"
    DATABASE_URL: str = "sqlite:///./test02.db"
    POSTGRES_URL: str = "postgresql+psycopg2://postgres:postgres@localhost/test03"
    user: str = "postgres"
    password : str = "postgres"

settings = Settings()