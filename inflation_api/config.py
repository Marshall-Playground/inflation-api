"""Configuration management for the inflation API."""


from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Application settings
    app_name: str = "Inflation Rate API"
    app_version: str = "0.1.0"
    debug: bool = False

    # API settings
    api_v1_prefix: str = "/api/v1"

    # Data settings
    inflation_data_path: str = "data/inflation_data.csv"

    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False

    # Logging settings
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False


def get_settings() -> Settings:
    """Get application settings (cached)."""
    return Settings()


# Global settings instance
settings = get_settings()
