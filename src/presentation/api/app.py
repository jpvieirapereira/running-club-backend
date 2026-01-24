from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.infrastructure.config import settings, logger
from src.infrastructure.container import Container
from src.infrastructure.aws import initialize_aws_resources
from src.presentation.api.v1 import api_router
from src.presentation.middleware import error_handler_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting application...")
    
    # Initialize AWS resources
    await initialize_aws_resources()
    
    logger.info("Application started successfully")
    yield
    logger.info("Shutting down application...")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    
    # Create container
    container = Container()
    container.wire(modules=[
        "src.presentation.api.v1.auth",
        "src.presentation.api.dependencies",
    ])
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.app_name,
        description="Clean Architecture Backend with FastAPI",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan
    )
    
    # Add container to app state
    app.state.container = container
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add error handler middleware
    app.middleware("http")(error_handler_middleware)
    
    # Include routers
    app.include_router(api_router, prefix=settings.api_v1_prefix)
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}
    
    return app
