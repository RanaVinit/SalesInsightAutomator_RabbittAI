"""Health check endpoint."""

from fastapi import APIRouter

from app.models.schemas import HealthResponse

router = APIRouter(tags=["Health"])


@router.get(
    "/api/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Returns the health status of the API service.",
)
async def health_check():
    """Check if the API is running and healthy."""
    return HealthResponse()
