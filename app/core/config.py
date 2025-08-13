"""
Application configuration using Pydantic settings.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Base configuration
    BASE_URL: str
    
    # WordPress configuration
    WP_USERNAME: str
    WP_APP_PASSWORD: str
    WP_AUTH_TYPE: str = "basic"
    
    # WooCommerce configuration
    WC_CONSUMER_KEY: str
    WC_CONSUMER_SECRET: str
    
    # Scheduler configuration
    ENABLE_SCHEDULER: bool = False
    SYNC_CRON: str = "*/15 * * * *"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings() 