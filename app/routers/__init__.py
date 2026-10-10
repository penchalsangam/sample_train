"""API Routers package."""

from app.routers.tasks import router as tasks_router
from app.routers.stats import router as stats_router

__all__ = ["tasks_router", "stats_router"]
