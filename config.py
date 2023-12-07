from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "New API"
    admin_email: str = "ponOlgap@gmail.com"
    DATABASE_URL: str = "sqlite:///./test02.db"

settings = Settings()