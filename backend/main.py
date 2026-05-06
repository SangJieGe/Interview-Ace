"""
Interview Ace — Backend Entry Point

FastAPI server that:
1. Serves WebSocket connections for real-time audio streaming
2. Provides REST API for knowledge base management
3. Orchestrates dual-agent pipeline (Voice Agent → Knowledge Agent)

Usage:
    uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from backend.api.routes import router as api_router
from backend.api.ws_routes import router as ws_router
from backend.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle."""
    logger.info("🚀 Interview Ace backend starting...")
    logger.info(f"   LLM Provider: {settings.LLM_PROVIDER}")
    logger.info(f"   Whisper Model: {settings.WHISPER_MODEL}")
    logger.info(f"   Vector DB: {settings.VECTOR_DB}")

    # TODO: Initialize agents, load voice profile, connect vector DB

    yield

    logger.info("👋 Shutting down Interview Ace backend...")


app = FastAPI(
    title="Interview Ace API",
    description="AI-powered real-time interview assistant",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS — allow Electron frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "app://."],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routes
app.include_router(api_router, prefix="/api")
app.include_router(ws_router)


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "interview-ace"}
