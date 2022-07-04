from typing import Optional, Dict, Any

from pydantic import BaseSettings, PostgresDsn, validator


COMMAND_LOCATIONS = [
    "core",
    "universities"
]


class Settings(BaseSettings):
    PROJECT_NAME: str = "api"

    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    PG_DNS: Optional[PostgresDsn] = None

    @validator("PG_DNS", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    BACKEND_CORS_ORIGINS: str

    JWT_TOKEN_EXP_MINUTES: int = 15

    BUILDINGS_MAX_BYTES_IMAGE_SIZE: int = 2193463


    SUPER_USER_EMAIL: str
    SUPER_USER_PASSWORD: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
