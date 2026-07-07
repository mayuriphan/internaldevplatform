import os 
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "idp-service-broker"
    APP_VERSION: str = "1.0.0"

    API_PREFIX: str = "/api/v1"

    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "idp")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")

    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))

    AWS_REGION: str = "ap-south-1"

    SQS_DLQ_URL: str = os.getenv("SQS_DLQ_URL", "")
    SQS_JOBQ_URL: str = os.getenv("SQS_JOBQ_URL", "")

    RATE_LIMIT_PER_MINUTE: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()