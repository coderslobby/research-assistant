import os
import sentry_sdk
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.logger import logger, setup_logger
from api.routes import router
from app.core.limiter import limiter
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from app.core.middleware import TraceIDMiddleware

os.makedirs("logs", exist_ok=True)
setup_logger()

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    environment=settings.APP_ENV
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    logger.info(f"Starting {settings.APP_NAME} in {settings.APP_ENV} mode")
    
    logger.info("Application started successfully")
    
    yield  # application runs here
    
    # shutdown
    logger.info("Shutting down application")
    logger.info("Application shut down successfully")

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/docs" if settings.APP_ENV == "development" else None,
    redoc_url=None,
    lifespan=lifespan
)

app.add_middleware(TraceIDMiddleware)
app.include_router(router)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "env": settings.APP_ENV
    }