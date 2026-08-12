from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "GovCaptureAI"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DEMO_RESET_ENABLED: bool = False

    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "govcaptureai"
    DATABASE_USER: str = "enriquelastrilla"
    DATABASE_PASSWORD: str = ""

    SAM_API_KEY: str = ""
    SAM_API_BASE_URL: str = "https://api.sam.gov/opportunities/v2/search"
    SAM_API_MODE: str = "mock"

    LLM_ROUTER_URL: str = "http://192.168.1.53:8080"
    CORS_ORIGINS: list[str] = [
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8001",
        "http://localhost:8001",
        "null",
    ]
    CORS_ORIGIN_REGEX: str | None = None

    @property
    def database_url(self) -> str:
        if self.DATABASE_PASSWORD:
            return (
                f"postgresql+psycopg2://{self.DATABASE_USER}:"
                f"{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:"
                f"{self.DATABASE_PORT}/{self.DATABASE_NAME}"
            )

        return (
            f"postgresql+psycopg2://{self.DATABASE_USER}@"
            f"{self.DATABASE_HOST}:{self.DATABASE_PORT}/"
            f"{self.DATABASE_NAME}"
        )

    class Config:
        env_file = ".env"


settings = Settings()
