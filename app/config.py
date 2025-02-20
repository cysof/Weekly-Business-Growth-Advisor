# import os
# from pydantic_settings import BaseSettings
# from dotenv import load_dotenv
# from typing import Dict, Any, Optional
# from dotenv import load_dotenv
# from typing import Dict, Any, Optional

# # Load environment variables from .env file if it exists
# load_dotenv()

# class APISettings(BaseSettings):
#     """Application settings loaded from environment variables."""
    
#     # API Configuration
#     API_TITLE: str = "Business Insights API"
#     API_DESCRIPTION: str = "API for generating business growth insights"
#     API_VERSION: str = "1.0.0"
#     DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
#     # Server Configuration
#     HOST: str = os.getenv("HOST", "0.0.0.0")
#     PORT: int = int(os.getenv("PORT", "8000"))
#     WORKERS: int = int(os.getenv("WORKERS", "1"))
#     RELOAD: bool = os.getenv("RELOAD", "False").lower() == "true"
    
#     # Authentication
#     SECRET_KEY: str = os.getenv("SECRET_KEY", "change_this_in_production")
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    
#     # External API Configuration
#     TELEX_WEBHOOK_URL: str = os.getenv("TELEX_WEBHOOK_URL", "https://ping.telex.im/v1/webhooks/01951969-ccbf-7ff0-be62-0c6286b0a6b7")
#     STRIPE_API_KEY: str = os.getenv("STRIPE_API_KEY", "")
#     STRIPE_API_BASE_URL: str = "https://api.stripe.com/v1/"
    
#     # Scheduler Configuration
#     SCHEDULER_TIMEZONE: str = os.getenv("SCHEDULER_TIMEZONE", "UTC")
#     INSIGHT_SCHEDULE_DAY: str = os.getenv("INSIGHT_SCHEDULE_DAY", "mon")
#     INSIGHT_SCHEDULE_HOUR: int = int(os.getenv("INSIGHT_SCHEDULE_HOUR", "9"))
    
#     # Rate Limiting
#     RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
#     RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # seconds
    
#     # Logging Configuration
#     LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
#     LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
#     # Metrics thresholds
#     REVENUE_SIGNIFICANT_DROP_THRESHOLD: float = float(os.getenv("REVENUE_SIGNIFICANT_DROP_THRESHOLD", "-15.0"))
#     REVENUE_SIGNIFICANT_GROWTH_THRESHOLD: float = float(os.getenv("REVENUE_SIGNIFICANT_GROWTH_THRESHOLD", "10.0"))
    
#     class Config:
#         env_file = ".env"
#         case_sensitive = True

# # Create a singleton instance
# settings = APISettings()

# # Configure logging based on settings
# import logging
# logging.basicConfig(
#     level=getattr(logging, settings.LOG_LEVEL),
#     format=settings.LOG_FORMAT
# )

# def get_settings() -> APISettings:
#     """Dependency for getting settings."""
#     return settings