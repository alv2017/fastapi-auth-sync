from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter, status

from .apps.auth.routes import router as auth_router
from .apps.users.routes import router as users_router
from .config import settings
from .loggers import api_logger


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    from api.db.connectors import db_engine

    api_logger.info(
        f"Starting the application server: {settings.run.host}:{settings.run.port}"
    )
    api_logger.info(f"Application mode: {settings.run.mode}")
    api_logger.info(f"Application DB URL: {settings.db.url}")
    api_logger.info(f"DB Engine: {db_engine}")
    api_logger.info(f"DB Engine Pool Size: {db_engine.pool.size()}")
    yield
    api_logger.info("Shutting the application server down.")
    db_engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.get("/", tags=["welcome"])
def welcome():
    return {
        "message": "Welcome!",
    }


main_router = APIRouter(tags=["main"])


@main_router.get("/health/", status_code=status.HTTP_200_OK)
def health_check():
    return {
        "status": "OK",
    }


app.include_router(main_router, prefix=settings.api_prefix)
app.include_router(auth_router, prefix=settings.api_prefix)
app.include_router(users_router, prefix=settings.api_prefix)
