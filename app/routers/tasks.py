"""Task CRUD and filtering endpoints."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models.task import Task
from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskListResponse,
    TaskStatus,
    TaskPriority,
)

router = APIRouter()


def _format_tags_to_db(tags: list) -> str:
    """Helper to convert list of tags into a normalized comma-delimited string."""
    if not tags:
        return ""
    clean = [t.strip().lower() for t in tags if t.strip()]
    return ",".join(sorted(set(clean)))


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Creates a new task with given title, description, priority, due date, and tags.",
)
def create_task(task_in: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task."""
    db_task = Task(
        title=task_in.title.strip(),
        description=task_in.description.strip() if task_in.description else None,
        priority=task_in.priority.value,
        status="todo",
        due_date=task_in.due_date,
        tags=_format_tags_to_db(task_in.tags),
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get(
    "",
    response_model=TaskListResponse,
    summary="List all tasks",
    description="Retrieve tasks with optional filters (status, priority, search term, tag) and pagination.",
)
def list_tasks(
    status_filter: Optional[TaskStatus] = Query(None, alias="status", description="Filter by task status"),
    priority_filter: Optional[TaskPriority] = Query(None, alias="priority", description="Filter by priority"),
    search: Optional[str] = Query(None, min_length=1, description="Search keyword in title or description"),
    tag: Optional[str] = Query(None, description="Filter by specific tag"),
    skip: int = Query(0, ge=0, description="Number of items to skip for pagination"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of items to return"),
    db: Session = Depends(get_db),
):
    """List tasks with filtering and pagination."""
    query = db.query(Task)

    if status_filter:
        query = query.filter(Task.status == status_filter.value)
    if priority_filter:
        query = query.filter(Task.priority == priority_filter.value)
    if search:
        search_pattern = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Task.title.ilike(search_pattern),
                Task.description.ilike(search_pattern),
            )
        )
    if tag:
        tag_pattern = f"%{tag.strip().lower()}%"
        query = query.filter(Task.tags.ilike(tag_pattern))

    total = query.count()
    tasks = query.order_by(Task.id.desc()).offset(skip).limit(limit).all()

    return TaskListResponse(
        items=tasks,
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get task by ID",
    description="Retrieve the complete details of a specific task by its ID.",
)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get single task details."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Full update of a task",
    description="Replace/update all fields of a specific task.",
)
def update_task_full(
    task_id: int,
    task_in: TaskCreate,
    status_val: TaskStatus = Query(TaskStatus.todo, description="Status of the task"),
    db: Session = Depends(get_db),
):
    """Fully update an existing task."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )

    task.title = task_in.title.strip()
    task.description = task_in.description.strip() if task_in.description else None
    task.priority = task_in.priority.value
    task.status = status_val.value
    task.due_date = task_in.due_date
    task.tags = _format_tags_to_db(task_in.tags)

    db.commit()
    db.refresh(task)
    return task


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Partial update of a task",
    description="Update only specific fields of a task without affecting other fields.",
)
def update_task_partial(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
):
    """Partially update an existing task."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )

    update_data = task_in.model_dump(exclude_unset=True)

    if "title" in update_data and update_data["title"] is not None:
        task.title = update_data["title"].strip()
    if "description" in update_data:
        task.description = update_data["description"].strip() if update_data["description"] else None
    if "status" in update_data and update_data["status"] is not None:
        task.status = update_data["status"].value
    if "priority" in update_data and update_data["priority"] is not None:
        task.priority = update_data["priority"].value
    if "due_date" in update_data:
        task.due_date = update_data["due_date"]
    if "tags" in update_data and update_data["tags"] is not None:
        task.tags = _format_tags_to_db(update_data["tags"])

    db.commit()
    db.refresh(task)
    return task


@router.patch(
    "/{task_id}/toggle",
    response_model=TaskResponse,
    summary="Toggle task completion",
    description="Quickly toggle a task's status between completed and todo.",
)
def toggle_task(task_id: int, db: Session = Depends(get_db)):
    """Toggle status between completed and todo."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )

    task.status = "todo" if task.status == "completed" else "completed"
    db.commit()
    db.refresh(task)
    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Permanently delete a task by its ID.",
)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )

    db.delete(task)
    db.commit()
    return None
