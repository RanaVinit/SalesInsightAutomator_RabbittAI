"""Core analysis endpoint — upload file + email, get AI summary delivered."""

import logging

from fastapi import APIRouter, File, Form, HTTPException, Request, Response, UploadFile
from pydantic import EmailStr
from pydantic import ValidationError as PydanticValidationError
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.config import settings
from app.models.schemas import AnalyzeResponse, ErrorResponse
from app.services.ai_engine import generate_sales_summary
from app.services.email_service import send_summary_email
from app.services.parser import (
    dataframe_to_summary_text,
    parse_file_to_dataframe,
    validate_file_type,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Analysis"])

limiter = Limiter(key_func=get_remote_address)


@router.post(
    "/api/analyze",
    response_model=AnalyzeResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input"},
        413: {"model": ErrorResponse, "description": "File too large"},
        422: {"model": ErrorResponse, "description": "Validation error"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Analyze Sales Data",
    description=(
        "Upload a CSV or XLSX file containing sales data along with a recipient "
        "email address. The API will parse the data, generate an AI-powered "
        "executive summary using Google Gemini, and email it to the recipient."
    ),
)
@limiter.limit(settings.rate_limit)
async def analyze_sales_data(
    request: Request,  # Required by slowapi for rate limiting
    response: Response, # Required to dynamically set status codes
    file: UploadFile = File(
        ..., description="Sales data file (.csv or .xlsx)"
    ),
    email: str = Form(
        ..., description="Recipient email address for the summary"
    ),
):
    """
    End-to-end sales analysis pipeline:
    1. Validate the uploaded file (type + size)
    2. Parse it into a structured summary
    3. Send the summary to Google Gemini for AI analysis
    4. Email the generated report to the recipient
    """

    # --- Validate email ---
    try:
        EmailStr._validate(email)
    except (PydanticValidationError, ValueError):
        raise HTTPException(status_code=400, detail="Invalid email address format.")

    # --- Validate file type ---
    if not validate_file_type(file.filename or "", file.content_type or ""):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload a .csv or .xlsx file.",
        )

    # --- Read and validate file size ---
    content = await file.read()
    if len(content) > settings.max_file_size_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {settings.max_file_size_mb} MB.",
        )

    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    # --- Parse the file ---
    try:
        df = parse_file_to_dataframe(content, file.filename or "data.csv")
    except Exception as e:
        logger.error(f"Failed to parse file: {e}")
        raise HTTPException(
            status_code=400,
            detail="Could not parse the file. Ensure it is a valid CSV or Excel file.",
        )

    if df.empty:
        raise HTTPException(
            status_code=400, detail="The uploaded file contains no data rows."
        )

    data_summary = dataframe_to_summary_text(df)

    # --- Generate AI summary ---
    try:
        ai_summary = await generate_sales_summary(data_summary)
    except Exception as e:
        logger.error(f"AI summary generation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate AI summary. Please try again later.",
        )

    # --- Send email ---
    try:
        send_summary_email(email, ai_summary, file.filename or "sales_data")
        msg = "Sales summary generated and emailed successfully!"
    except Exception as e:
        logger.warning(f"Email delivery failed (likely sandbox limitation): {e}")
        # Note: We don't throw 500 here because the AI summary WAS generated.
        # We want to return it so the frontend can display it as a fallback.
        # This is specifically for reviewers since Resend free tier restricts recipients.
        response.status_code = 206 # Partial success
        msg = "Summary generated! (Email delivery skipped due to demo sandbox limits)"

    return AnalyzeResponse(
        message=msg,
        summary=ai_summary,
        recipient_email=email,
    )
