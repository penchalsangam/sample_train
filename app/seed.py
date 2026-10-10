"""Script to seed initial demo tasks into the database."""

from datetime import datetime, timedelta, timezone
from app.database import SessionLocal, Base, engine
from app.models.task import Task


def seed_data():
    """Populate database with sample tasks if empty."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        existing_count = db.query(Task).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} tasks. Skipping seeding.")
            return

        now = datetime.now(timezone.utc)

        sample_tasks = [
            Task(
                title="Initialize FastAPI application scaffold",
                description="Create folder structure with routers, schemas, models, and config.",
                status="completed",
                priority="high",
                due_date=now - timedelta(days=2),
                tags="setup,fastapi,architecture",
            ),
            Task(
                title="Design SQLAlchemy database models & migrations",
                description="Define Task model with proper datatypes, indices, and constraints.",
                status="completed",
                priority="urgent",
                due_date=now - timedelta(days=1),
                tags="database,sqlalchemy,orm",
            ),
            Task(
                title="Implement RESTful CRUD endpoints & validation",
                description="Build Pydantic v2 schemas and endpoints for tasks with pagination and filters.",
                status="in_progress",
                priority="high",
                due_date=now + timedelta(days=2),
                tags="backend,api,pydantic",
            ),
            Task(
                title="Develop interactive single-page dashboard",
                description="Create modern frontend with Tailwind CSS, responsive cards, and live API fetch.",
                status="in_progress",
                priority="medium",
                due_date=now + timedelta(days=3),
                tags="frontend,ui,tailwind",
            ),
            Task(
                title="Write pytest test suite for all endpoints",
                description="Cover happy paths, 404 handling, input validation, and stats calculation.",
                status="todo",
                priority="medium",
                due_date=now + timedelta(days=5),
                tags="testing,pytest,quality",
            ),
            Task(
                title="Review OpenAPI specifications and Swagger docs",
                description="Verify endpoint docstrings, descriptions, example payloads, and status codes.",
                status="todo",
                priority="low",
                due_date=now + timedelta(days=7),
                tags="docs,openapi,swagger",
            ),
        ]

        db.add_all(sample_tasks)
        db.commit()
        print(f"Successfully seeded {len(sample_tasks)} sample tasks!")
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
