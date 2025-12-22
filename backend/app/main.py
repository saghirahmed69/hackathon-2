"""
FastAPI application entry point.
Phase II - Full-Stack Todo Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime

from app.config import settings
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    print("🚀 Starting up...")
    await init_db()
    print("✅ Database initialized")
    yield
    # Shutdown
    print("👋 Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Todo API - Phase II",
    description="Full-stack todo application with authentication",
    version="2.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:3000",
        "http://localhost:3001",  # Support both common Next.js ports
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request logging middleware for debugging
from fastapi import Request
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests for debugging."""
    logger.info(f"🔍 {request.method} {request.url.path}")
    logger.info(f"   Headers: {dict(request.headers)}")
    response = await call_next(request)
    logger.info(f"   Response: {response.status_code}")
    return response


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2.0.0",
    }


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "Todo API - Phase II",
        "docs": "/docs",
        "health": "/health",
    }


# API routers
from app.api import auth, tasks

app.include_router(auth.router)
app.include_router(tasks.router)
