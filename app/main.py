# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config.settings import get_settings
from .api.v1.endpoints import agents, configs, metrics, logs
from .core.database import engine, Base

settings = get_settings()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="""
    Nginx Agent Manager API allows you to manage and monitor nginx instances across your infrastructure.
    You can register agents, manage configurations, collect metrics, and monitor logs.
    """,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
api_v1_prefix = settings.API_V1_STR

# Include routers with proper prefixes
app.include_router(
    agents.router,
    prefix=api_v1_prefix,
    tags=["Agents"]
)

app.include_router(
    configs.router,
    prefix=f"{api_v1_prefix}/configs",
    tags=["Nginx Configurations"]
)

app.include_router(
    metrics.router,
    prefix=f"{api_v1_prefix}/metrics",
    tags=["Metrics"]
)

app.include_router(
    logs.router,
    prefix=f"{api_v1_prefix}/logs",
    tags=["Logs"]
)

@app.get("/", tags=["Health Check"])
def root():
    """
    Root endpoint for health check
    """
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "app_name": settings.APP_NAME
    }

@app.get("/health", tags=["Health Check"])
def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "database": "connected" if engine else "disconnected"
    }