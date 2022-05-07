from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    PROJECT_NAME: str = "api"

    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    PG_DNS: PostgresDsn = "postgres://user:pass@localhost:5432/db"

    BACKEND_CORS_ORIGINS: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
