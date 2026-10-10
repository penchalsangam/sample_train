"""Pydantic schemas for data validation and serialization."""

from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict
from pydantic import BaseModel, Field, ConfigDict, field_validator


class TaskStatus(str, Enum):
    """Enumeration of allowed task statuses."""
    todo = "todo"
    in_progress = "in_progress"
    completed = "completed"


class TaskPriority(str, Enum):
    """Enumeration of allowed task priorities."""
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class TaskBase(BaseModel):
    """Base schema with common task fields."""
    title: str = Field(
        ...,
        min_length=1,
        max_length=150,
        description="Title of the task",
        examples=["Build authentication system"]
    )
    description: Optional[str] = Field(
        None,
        max_length=2000,
        description="Detailed description of the task",
        examples=["Implement OAuth2 password bearer with JWT tokens."]
    )
    priority: TaskPriority = Field(
        default=TaskPriority.medium,
        description="Task priority level"
    )
    due_date: Optional[datetime] = Field(
        None,
        description="Due date and time in ISO 8601 format (e.g., 2026-12-31T23:59:59)"
    )
    tags: List[str] = Field(
        default_factory=list,
        description="List of categories or tags associated with the task",
        examples=[["backend", "security", "v1"]]
    )

    @field_validator("tags", mode="before")
    @classmethod
    def parse_tags(cls, value):
        """Parse tags whether supplied as a comma-separated string or list."""
        if isinstance(value, str):
            if not value.strip():
                return []
            return [t.strip() for t in value.split(",") if t.strip()]
        if isinstance(value, (list, tuple, set)):
            return [str(t).strip() for t in value if str(t).strip()]
        return []


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating an existing task. All fields are optional."""
    title: Optional[str] = Field(None, min_length=1, max_length=150)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None

    @field_validator("tags", mode="before")
    @classmethod
    def parse_tags(cls, value):
        if value is None:
            return None
        if isinstance(value, str):
            if not value.strip():
                return []
            return [t.strip() for t in value.split(",") if t.strip()]
        if isinstance(value, (list, tuple, set)):
            return [str(t).strip() for t in value if str(t).strip()]
        return []


class TaskResponse(TaskBase):
    """Schema for task response returned to clients."""
    id: int = Field(..., description="Unique task identifier")
    status: TaskStatus = Field(..., description="Current status of the task")
    created_at: datetime = Field(..., description="Timestamp of task creation")
    updated_at: datetime = Field(..., description="Timestamp of last update")

    model_config = ConfigDict(from_attributes=True)


class TaskListResponse(BaseModel):
    """Paginated list of tasks response."""
    items: List[TaskResponse]
    total: int
    skip: int
    limit: int


class TaskStatsResponse(BaseModel):
    """Summary statistics for tasks."""
    total: int
    completed: int
    in_progress: int
    todo: int
    completion_rate: float = Field(..., description="Percentage of completed tasks (0-100)")
    by_priority: Dict[str, int]
    overdue: int = Field(..., description="Number of tasks that are past due and not completed")
