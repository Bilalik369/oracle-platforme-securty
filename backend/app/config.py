from functools import lru_cache
from typing import List
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_file_encoding="utf-8"
    )

    APP_NAME: str = "Oracle Supervision Platform"
    DEBUG: bool = True
    API_PREFIX: str = "/api"

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "oracle_supervisor"
    POSTGRES_PASSWORD: str = "Oracle123"
    POSTGRES_DB: str = "oracle_monitoring"

    ORACLE_HOST: str = "localhost"
    ORACLE_PORT: int = 1521
    ORACLE_SERVICE: str = "XEPDB1"
    ORACLE_USER: str = "system"
    ORACLE_PASSWORD: str = "Oracle123"
    ORACLE_SIMULATION_MODE: bool = True

    COLLECTOR_ENABLED: bool = True
    COLLECTOR_INTERVAL_SECONDS: int = 60

    ML_MODEL_DIR: str = "./ml_models"
    ML_MIN_TRAINING_SAMPLES: int = 50
    ANOMALY_CONTAMINATION: float = 0.05

    THRESHOLD_CPU_WARNING: float = 75
    THRESHOLD_CPU_CRITICAL: float = 90
    THRESHOLD_TABLESPACE_WARNING: float = 80
    THRESHOLD_TABLESPACE_CRITICAL: float = 90
    THRESHOLD_SESSIONS_WARNING: int = 150
    THRESHOLD_SESSIONS_CRITICAL: int = 250

    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    @property
    def cors_list(self) -> List[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]

    @property
    def postgres_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def oracle_dsn(self) -> str:
        return f"{self.ORACLE_HOST}:{self.ORACLE_PORT}/{self.ORACLE_SERVICE}"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()