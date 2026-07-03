from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.database.session import engine


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


@app.get("/")
def root():
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/health/database")
def database_health_check():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            value = result.scalar()

        return {
            "status": "healthy",
            "database": "connected",
            "result": value,
        }

    except Exception as error:
        return {
            "status": "unhealthy",
            "database": "not connected",
            "error": str(error),
        }