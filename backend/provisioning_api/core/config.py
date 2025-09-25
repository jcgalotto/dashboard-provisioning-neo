# backend/provisioning_api/core/config.py
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

class Settings(BaseSettings):
    uvicorn_host: str = "127.0.0.1"
    uvicorn_port: int = 8000
    api_prefix: str = "/api"
    cors_origins: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    # hace que lea backend/.env automáticamente
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _csv(cls, v):
        if isinstance(v, str):
            return [s.strip() for s in v.split(",") if s.strip()]
        return v

_settings = Settings()

def get_settings() -> Settings:
    return _settings
