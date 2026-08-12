from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.v1.companies import router as companies_router
from app.api.v1.opportunities import router as opportunities_router
from app.api.v1.sam import router as sam_router
from app.core.config import settings
from app.database.session import engine


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(companies_router, prefix="/api/v1")
app.include_router(opportunities_router, prefix="/api/v1")
app.include_router(sam_router, prefix="/api/v1")


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
