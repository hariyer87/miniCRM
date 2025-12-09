from functools import lru_cache
import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "MiniCRM Clinic"
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./data.db")
    secret_key: str = os.getenv("SECRET_KEY", "super-secret-key")
    access_token_expire_minutes: int = 60 * 24
    algorithm: str = "HS256"
    dicom_inbox_dir: str = os.getenv("DICOM_INBOX_DIR", "./dicom_inbox")
    dicom_archive_dir: str = os.getenv("DICOM_ARCHIVE_DIR", "./dicom_archive")

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
