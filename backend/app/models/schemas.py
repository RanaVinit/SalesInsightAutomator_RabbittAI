"""Pydantic models for API request/response schemas."""

from pydantic import BaseModel


class AnalyzeResponse(BaseModel):
    """Response returned on successful analysis."""

    success: bool = True
    message: str
    summary: str
    recipient_email: str


class ErrorResponse(BaseModel):
    """Standard error response."""

    success: bool = False
    detail: str


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "healthy"
    service: str = "Sales Insight Automator API"
    version: str = "1.0.0"
