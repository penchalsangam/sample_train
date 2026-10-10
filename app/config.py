"""Application Configuration Module."""

import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings:
    """Application settings with environment variable fallbacks."""

    APP_NAME: str = "TaskFlow API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = (
        "A feature-rich, high-performance RESTful Task & Workflow Management API "
        "built with FastAPI, Pydantic, and SQLite/SQLAlchemy."
    )
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")

    # Database configuration (SQLite by default)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'taskflow.db'}"
    )

    # Server settings
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))


settings = Settings()
