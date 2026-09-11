from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PULSEFORGE_", env_file=".env", extra="ignore")

    env: str = "development"
    ai_provider: str = "mock"
    database_url: str = "postgresql+psycopg://pulseforge:pulseforge@localhost:5432/pulseforge"
    redis_url: str = "redis://localhost:6379/0"
    nats_url: str = "nats://localhost:4222"
    max_download_bytes: int = 5_000_000
    allowed_content_types: str = (
        "text/html,application/xml,text/xml,application/rss+xml,application/atom+xml,"
        "application/json,text/plain"
    )

    @property
    def content_types(self) -> set[str]:
        return {item.strip().lower() for item in self.allowed_content_types.split(",") if item.strip()}


@lru_cache
def get_settings() -> Settings:
    return Settings()
