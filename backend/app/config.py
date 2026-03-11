"""Application configuration loaded from environment variables."""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Central configuration for the Sales Insight Automator backend."""

    # --- API Keys ---
    gemini_api_key: str = Field(..., description="Google Gemini API key")
    resend_api_key: str = Field(..., description="Resend API key for email delivery")

    # --- CORS ---
    allowed_origins: str = Field(
        "http://localhost:5173,http://localhost:3000",
        description="Comma-separated list of allowed CORS origins",
    )

    # --- File Upload ---
    max_file_size_mb: int = Field(10, description="Maximum upload file size in MB")

    # --- Rate Limiting ---
    rate_limit: str = Field(
        "10/minute", description="Rate limit for the analyze endpoint"
    )

    # --- Email ---
    from_email: str = Field(
        "Sales Insight <onboarding@resend.dev>",
        description="Sender email address",
    )

    # --- AI Model ---
    gemini_model: str = Field(
        "gemini-2.0-flash", description="Gemini model to use"
    )

    @property
    def origins_list(self) -> list[str]:
        """Parse comma-separated origins into a list."""
        return [o.strip() for o in self.allowed_origins.split(",")]

    @property
    def max_file_size_bytes(self) -> int:
        """Convert MB to bytes."""
        return self.max_file_size_mb * 1024 * 1024

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
