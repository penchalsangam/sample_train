"""Task SQLAlchemy ORM Model."""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.database import Base


def utc_now():
    """Return the current UTC datetime."""
    return datetime.now(timezone.utc)


class Task(Base):
    """Database model representing a task in the TaskFlow system."""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(150), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="todo", nullable=False, index=True)
    priority = Column(String(20), default="medium", nullable=False, index=True)
    due_date = Column(DateTime, nullable=True)
    tags = Column(String(255), default="", nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"
