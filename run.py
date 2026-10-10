"""Entry point script to run the TaskFlow FastAPI application."""

import sys
import uvicorn
from app.config import settings
from app.seed import seed_data


def main():
    """Seed sample data if needed, then run the development server."""
    print("====================================================")
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"📍 Web Dashboard:   http://{settings.HOST}:{settings.PORT}")
    print(f"📖 Swagger Docs:    http://{settings.HOST}:{settings.PORT}/docs")
    print(f"📑 ReDoc Docs:      http://{settings.HOST}:{settings.PORT}/redoc")
    print("====================================================")

    # Seed demo data if database is new
    try:
        seed_data()
    except Exception as e:
        print(f"⚠️  Note: Could not seed data automatically: {e}")

    # Start Uvicorn server
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )


if __name__ == "__main__":
    main()
