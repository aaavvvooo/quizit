from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.routers.health import router as health_router
from app.api.routers.auth_router import router as auth_router


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(title=settings.app_name)
    app.include_router(health_router)
    app.include_router(auth_router)

    return app


app = create_app()
