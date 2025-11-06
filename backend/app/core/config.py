from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    DATABASE_URL: str = "sqlite:///./clinic.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application
    APP_NAME: str = "Doctor Appointment System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # CORS - Default includes GitHub Pages and localhost
    CORS_ORIGINS: str = "https://luciansans.github.io,http://localhost:3000,http://localhost:8080"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert CORS origins string to list."""
        origins = [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        # Filter out empty strings
        return [origin for origin in origins if origin]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"


settings = Settings()