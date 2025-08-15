"""
Configuration management for the application.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration class."""
    
    # Application settings
    APP_NAME: str = "Demo3"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # API settings
    API_BASE_URL: str = os.getenv("API_BASE_URL", "https://api.example.com")
    API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "30"))
    
    # Database settings
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    
    # Logging settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: Optional[str] = os.getenv("LOG_FILE")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration settings."""
        required_settings = [
            cls.APP_NAME,
            cls.APP_VERSION,
        ]
        
        return all(setting for setting in required_settings)