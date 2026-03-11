"""
Sales Insight Automator — FastAPI Backend
==========================================
Main application entry point. Configures CORS, rate limiting, and mounts routers.
"""

import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.routers import analyze, health

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

# --- App ---
app = FastAPI(
    title="Sales Insight Automator API",
    description=(
        "Upload sales data (CSV/XLSX) and receive an AI-generated executive summary "
        "delivered straight to your inbox. Powered by Google Gemini."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Rate limiting ---
app.state.limiter = analyze.limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- Global exception handler ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch-all handler to prevent stack traces from leaking."""
    logging.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"success": False, "detail": "An internal server error occurred."},
    )


# --- Routers ---
app.include_router(health.router)
app.include_router(analyze.router)
