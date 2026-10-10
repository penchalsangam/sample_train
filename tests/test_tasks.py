"""Automated unit and integration tests for TaskFlow FastAPI application."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

# Set up an isolated in-memory SQLite database for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """Dependency override that provides the in-memory test database session."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override the get_db dependency in the FastAPI application
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_test_db():
    """Create fresh schema before each test and drop after."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    """Test client fixture."""
    with TestClient(app) as c:
        yield c


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "TaskFlow" in data["app"]


def test_create_task(client):
    """Test creating a new task."""
    payload = {
        "title": "Build user auth",
        "description": "JWT-based authentication flow",
        "priority": "high",
        "tags": ["backend", "security"],
    }
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["title"] == payload["title"]
    assert data["status"] == "todo"
    assert data["priority"] == "high"
    assert "backend" in data["tags"]


def test_create_task_validation_error(client):
    """Test that missing or empty title raises a 422 validation error."""
    response = client.post("/api/tasks", json={"title": ""})
    assert response.status_code == 422


def test_list_tasks_and_pagination(client):
    """Test listing tasks with pagination."""
    # Create 3 tasks
    for i in range(3):
        client.post("/api/tasks", json={"title": f"Task {i}"})

    response = client.get("/api/tasks?skip=0&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["items"]) == 2
    assert data["limit"] == 2


def test_filter_by_status_and_priority(client):
    """Test filtering tasks by status and priority."""
    client.post("/api/tasks", json={"title": "High task", "priority": "high"})
    client.post("/api/tasks", json={"title": "Low task", "priority": "low"})

    response = client.get("/api/tasks?priority=high")
    assert response.status_code == 200
    items = response.json()["items"]
    assert len(items) == 1
    assert items[0]["priority"] == "high"


def test_search_tasks(client):
    """Test searching tasks by title keyword."""
    client.post("/api/tasks", json={"title": "Fix bug in payment gateway"})
    client.post("/api/tasks", json={"title": "Update UI color scheme"})

    response = client.get("/api/tasks?search=payment")
    assert response.status_code == 200
    items = response.json()["items"]
    assert len(items) == 1
    assert "payment" in items[0]["title"].lower()


def test_get_task_by_id(client):
    """Test retrieving a single task by ID."""
    created = client.post("/api/tasks", json={"title": "Specific Task"}).json()
    task_id = created["id"]

    response = client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Specific Task"


def test_get_task_not_found(client):
    """Test 404 response when querying a non-existent task ID."""
    response = client.get("/api/tasks/99999")
    assert response.status_code == 404


def test_partial_update_task(client):
    """Test PATCH endpoint for partial task updates."""
    created = client.post("/api/tasks", json={"title": "Old Title", "priority": "low"}).json()
    task_id = created["id"]

    patch_res = client.patch(
        f"/api/tasks/{task_id}",
        json={"title": "New Updated Title", "priority": "urgent"},
    )
    assert patch_res.status_code == 200
    updated = patch_res.json()
    assert updated["title"] == "New Updated Title"
    assert updated["priority"] == "urgent"


def test_toggle_task_status(client):
    """Test toggling task completion status."""
    created = client.post("/api/tasks", json={"title": "Toggle Me"}).json()
    task_id = created["id"]
    assert created["status"] == "todo"

    # Toggle to completed
    res1 = client.patch(f"/api/tasks/{task_id}/toggle")
    assert res1.status_code == 200
    assert res1.json()["status"] == "completed"

    # Toggle back to todo
    res2 = client.patch(f"/api/tasks/{task_id}/toggle")
    assert res2.status_code == 200
    assert res2.json()["status"] == "todo"


def test_delete_task(client):
    """Test deleting a task."""
    created = client.post("/api/tasks", json={"title": "Delete Me"}).json()
    task_id = created["id"]

    del_res = client.delete(f"/api/tasks/{task_id}")
    assert del_res.status_code == 204

    # Verify task is deleted
    get_res = client.get(f"/api/tasks/{task_id}")
    assert get_res.status_code == 404


def test_stats_endpoint(client):
    """Test analytics and statistics calculation endpoint."""
    # Create 2 todo, 1 completed
    t1 = client.post("/api/tasks", json={"title": "Task 1", "priority": "high"}).json()
    client.post("/api/tasks", json={"title": "Task 2", "priority": "low"})
    client.patch(f"/api/tasks/{t1['id']}/toggle")  # mark Task 1 completed

    res = client.get("/api/stats")
    assert res.status_code == 200
    stats = res.json()
    assert stats["total"] == 2
    assert stats["completed"] == 1
    assert stats["todo"] == 1
    assert stats["completion_rate"] == 50.0
    assert stats["by_priority"]["high"] == 1
    assert stats["by_priority"]["low"] == 1
