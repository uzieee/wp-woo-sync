"""
Application configuration settings.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Base configuration
    BASE_URL: Optional[str] = "https://eidcarosse.ch"
    
    # WordPress configuration (Application Passwords)
    WP_USERNAME: Optional[str] = "demo_user"
    WP_APP_PASSWORD: Optional[str] = "demo_password"
    WP_AUTH_TYPE: str = "basic"
    
    # WooCommerce configuration
    WC_CONSUMER_KEY: Optional[str] = "demo_consumer_key"
    WC_CONSUMER_SECRET: Optional[str] = "demo_consumer_secret"
    
    # Scheduler configuration
    ENABLE_SCHEDULER: bool = False
    SYNC_CRON: str = "*/15 * * * *"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings() 