# ⚡ TaskFlow API - Python FastAPI Mini Project

A modern, production-grade **Task & Workflow Management API** built with **FastAPI**, **Pydantic v2**, and **SQLAlchemy (SQLite)**. It includes a complete RESTful CRUD API, filtering & search, analytics, automated tests, and a built-in interactive **single-page dashboard** with Tailwind CSS.

---

## ✨ Features

- **🚀 FastAPI & ASGI**: Ultra-fast asynchronous REST framework with automated OpenAPI 3.0 specs.
- **🛡️ Pydantic v2 Data Validation**: Robust request and response validation with strict types, field constraints, and custom validators.
- **💾 SQLite + SQLAlchemy 2.0**: Zero-configuration database setup with ORM models and dependency-injected sessions (`Depends(get_db)`).
- **🔍 Advanced Query Filters**: Filter tasks by status (`todo`, `in_progress`, `completed`), priority (`low`, `medium`, `high`, `urgent`), search keyword, tags, and pagination (`skip`, `limit`).
- **📊 Real-time Analytics**: Built-in `/api/stats` endpoint calculating total tasks, completion percentage, overdue count, and priority breakdowns.
- **⏱️ Custom Middleware**: Automatic request timing with `X-Process-Time` header and configurable CORS support.
- **🎨 Interactive Web Dashboard**: Built-in responsive UI served directly at `http://127.0.0.1:8000` for creating, toggling, filtering, and managing tasks visually.
- **📖 Interactive API Docs**: Out-of-the-box Swagger UI (`/docs`) and ReDoc (`/redoc`).
- **🧪 Comprehensive Test Suite**: 11 automated unit and integration tests using `pytest` and `TestClient` with an isolated in-memory database.

---

## 📁 Project Architecture

```
e:\sample coding\
├── app/
│   ├── __init__.py          # App package initialization
│   ├── main.py              # FastAPI app instance, middleware, and route mounting
│   ├── config.py            # App configuration and settings
│   ├── database.py          # SQLAlchemy engine, session maker, and get_db dependency
│   ├── seed.py              # Demo data populator script
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # SQLAlchemy Task model
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── task.py          # Pydantic v2 schemas (validation & serialization)
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── tasks.py         # CRUD, search, filter, and toggle endpoints
│   │   └── stats.py         # Analytics & statistics endpoint
│   └── static/
│       └── index.html       # Single-Page web dashboard (Tailwind CSS)
├── tests/
│   ├── __init__.py
│   └── test_tasks.py        # Complete pytest suite with isolated test DB
├── run.py                   # One-click startup script (auto-seeds demo data)
├── requirements.txt         # Project dependencies
├── .gitignore               # Git ignore rules
└── README.md                # Project documentation
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure you have **Python 3.10+** installed on your system.

### 2. Create and Activate a Virtual Environment

**On Windows (PowerShell / Command Prompt):**
```powershell
python -m venv venv
venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
You can start the server using the included `run.py` script:
```bash
python run.py
```

*Alternatively, run directly via Uvicorn:*
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

---

## 🌐 Application URLs

Once running, open your browser to access:

| Destination | URL | Description |
| :--- | :--- | :--- |
| **Interactive Dashboard** | [http://127.0.0.1:8000](http://127.0.0.1:8000) | Live visual task manager UI |
| **Swagger UI Documentation** | [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) | Interactive API playground with "Try it out" |
| **ReDoc Documentation** | [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) | Clean, readable OpenAPI documentation |
| **System Health Check** | [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health) | API health & version check |

---

## 📡 API Endpoints Reference

### Tasks (`/api/tasks`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/tasks` | Create a new task (201 Created) |
| `GET` | `/api/tasks` | List tasks with pagination & filters (`status`, `priority`, `search`, `tag`) |
| `GET` | `/api/tasks/{task_id}` | Retrieve details of a specific task by ID |
| `PUT` | `/api/tasks/{task_id}` | Full update of an existing task |
| `PATCH` | `/api/tasks/{task_id}` | Partial update of task attributes |
| `PATCH` | `/api/tasks/{task_id}/toggle` | Quick-toggle task status between `todo` and `completed` |
| `DELETE` | `/api/tasks/{task_id}` | Delete a task (204 No Content) |

### Analytics & System

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/stats` | Overview analytics: total, completed, in-progress, overdue, priority breakdown |
| `GET` | `/health` | Application status and version |

---

## 💡 Example API Requests

### 1. Create a Task
```bash
curl -X POST "http://127.0.0.1:8000/api/tasks" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Design Database Schema",
       "description": "Create SQLAlchemy models for users and tasks",
       "priority": "high",
       "tags": ["backend", "database"]
     }'
```

### 2. List Tasks with Filters & Search
```bash
# Filter by priority and search keyword
curl "http://127.0.0.1:8000/api/tasks?priority=high&search=database"
```

### 3. Toggle Task Completion
```bash
curl -X PATCH "http://127.0.0.1:8000/api/tasks/1/toggle"
```

### 4. Fetch Analytics Summary
```bash
curl "http://127.0.0.1:8000/api/stats"
```

---

## 🧪 Running Automated Tests

Run the test suite using `pytest`:

```bash
pytest -v
```

The tests use an isolated in-memory SQLite database (`sqlite:///:memory:`), ensuring your local development data remains untouched.

---

## 📜 License
MIT License. Free to use, adapt, and build upon!
