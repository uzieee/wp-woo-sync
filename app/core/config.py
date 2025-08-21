from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    BASE_URL: Optional[str] = "https://eidcarosse.ch"
    
    WP_USERNAME: Optional[str] = "demo_user"
    WP_APP_PASSWORD: Optional[str] = "demo_password"
    WP_AUTH_TYPE: str = "basic"
    
    WC_CONSUMER_KEY: Optional[str] = "demo_consumer_key"
    WC_CONSUMER_SECRET: Optional[str] = "demo_consumer_secret"
    
    ENABLE_SCHEDULER: bool = False
    SYNC_CRON: str = "*/15 * * * *"
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings() 