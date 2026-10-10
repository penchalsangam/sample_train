"""Analytics and statistics endpoint for TaskFlow."""

from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.task import Task
from app.schemas.task import TaskStatsResponse

router = APIRouter()


@router.get(
    "",
    response_model=TaskStatsResponse,
    summary="Get task statistics",
    description="Calculate overview metrics including completion rates, status breakdown, and priority distributions.",
)
def get_task_statistics(db: Session = Depends(get_db)):
    """Calculate and return task overview analytics."""
    total = db.query(func.count(Task.id)).scalar() or 0
    completed = db.query(func.count(Task.id)).filter(Task.status == "completed").scalar() or 0
    in_progress = db.query(func.count(Task.id)).filter(Task.status == "in_progress").scalar() or 0
    todo = db.query(func.count(Task.id)).filter(Task.status == "todo").scalar() or 0

    completion_rate = round((completed / total * 100), 1) if total > 0 else 0.0

    # Count by priority
    priorities = ["low", "medium", "high", "urgent"]
    by_priority = {}
    for p in priorities:
        count = db.query(func.count(Task.id)).filter(Task.priority == p).scalar() or 0
        by_priority[p] = count

    # Overdue tasks
    now = datetime.now(timezone.utc)
    overdue = (
        db.query(func.count(Task.id))
        .filter(
            Task.due_date.isnot(None),
            Task.due_date < now,
            Task.status != "completed",
        )
        .scalar()
        or 0
    )

    return TaskStatsResponse(
        total=total,
        completed=completed,
        in_progress=in_progress,
        todo=todo,
        completion_rate=completion_rate,
        by_priority=by_priority,
        overdue=overdue,
    )
