from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PULSEFORGE_", env_file=".env", extra="ignore")

    env: str = "development"
    log_level: str = "INFO"
    demo_mode: bool = True
    repository_mode: str = "demo"
    auth_mode: str = "local"
    local_user_id: str = "local-analyst"
    local_user_email: str = "analyst@pulseforge.local"
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 480

    ai_provider: str = "mock"
    openai_api_key: str | None = None
    openai_model: str = "gpt-5.6"
    azure_openai_api_key: str | None = None
    azure_openai_endpoint: str | None = None
    azure_openai_deployment: str | None = None
    local_ai_base_url: str = "http://localhost:11434/v1"
    local_ai_model: str = "qwen3:8b"

    database_url: str = "postgresql+psycopg://pulseforge:pulseforge@localhost:5432/pulseforge"
    redis_url: str = "redis://localhost:6379/0"
    nats_url: str = "nats://localhost:4222"
    stream_name: str = "PULSEFORGE"
    stream_subject_prefix: str = "pulseforge"

    max_download_bytes: int = 5_000_000
    ingestion_timeout_seconds: float = 15.0
    max_redirects: int = 5
    upload_max_bytes: int = 10_000_000
    allowed_content_types: str = (
        "text/html,application/xml,text/xml,application/rss+xml,application/atom+xml,"
        "application/json,text/plain,application/pdf,text/markdown"
    )

    rate_limit_per_minute: int = 120
    enable_metrics: bool = True
    enable_tracing: bool = True
    otlp_endpoint: str | None = None
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    @property
    def content_types(self) -> set[str]:
        return {item.strip().lower() for item in self.allowed_content_types.split(",") if item.strip()}

    @property
    def cors_origin_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
