"""Main FastAPI Application Entrypoint."""

import time
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings, BASE_DIR
from app.database import engine, Base
from app.routers import tasks_router, stats_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler: sets up database tables on startup."""
    # Create all tables on startup
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    lifespan=lifespan,
    openapi_tags=[
        {
            "name": "Tasks",
            "description": "Operations on tasks: create, list, filter, search, update, toggle, and delete.",
        },
        {
            "name": "Analytics & Stats",
            "description": "Computed metrics, completion rates, and priority analytics.",
        },
    ],
)

# CORS Middleware to allow browser requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Custom middleware calculating request duration and attaching X-Process-Time."""
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    return response


# Include Routers
app.include_router(tasks_router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(stats_router, prefix="/api/stats", tags=["Analytics & Stats"])


# Static Dashboard at root path
INDEX_FILE = BASE_DIR / "app" / "static" / "index.html"


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def serve_dashboard():
    """Serves the interactive web UI dashboard."""
    if INDEX_FILE.exists():
        return FileResponse(INDEX_FILE)
    return HTMLResponse("<h1>TaskFlow API is running. Visit <a href='/docs'>/docs</a>.</h1>")


@app.get("/health", tags=["Health"], summary="System health check")
async def health_check():
    """Returns application status and version metadata."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }
