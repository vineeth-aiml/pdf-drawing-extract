from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///data/app.db"
    redis_url: str = "redis://localhost:6379/0"
    storage_dir: str = "data/storage"
    ocr_engine: str = "paddle"   # paddle | none
    render_dpi: int = 300
    pipeline_default: str = "final"

settings = Settings()
