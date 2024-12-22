# backend/app/core/config.py
from pydantic import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = ""Jewelry Scraper""
    VERSION: str = ""1.0.0""
    API_V1_STR: str = ""/api/v1""
    SECRET_KEY: str = os.getenv(""SECRET_KEY"", ""your-secret-key"")
    
    # Database
    POSTGRES_SERVER: str = os.getenv(""POSTGRES_SERVER"", ""localhost"")
    POSTGRES_USER: str = os.getenv(""POSTGRES_USER"", ""postgres"")
    POSTGRES_PASSWORD: str = os.getenv(""POSTGRES_PASSWORD"", """")
    POSTGRES_DB: str = os.getenv(""POSTGRES_DB"", ""jewelry_scraper"")
    SQLALCHEMY_DATABASE_URI: str = (
        f""postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}""
        f""@{POSTGRES_SERVER}/{POSTGRES_DB}""
    )
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [""http://localhost:3000""]
    
    # JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Scraping
    MAX_CONCURRENT_SCRAPES: int = 5
    SCRAPE_TIMEOUT: int = 300  # 5 minutes
    
    class Config:
        case_sensitive = True

settings = Settings()