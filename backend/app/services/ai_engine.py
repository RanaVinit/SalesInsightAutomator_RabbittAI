"""Service for generating AI-powered sales summaries using Google Gemini."""

import google.generativeai as genai

from app.config import settings

# Configure the Gemini client
genai.configure(api_key=settings.gemini_api_key)

SYSTEM_PROMPT = """You are a senior sales analyst at a Fortune 500 company. Your job is to
analyze raw sales data and produce a clear, professional executive summary.

Your summary MUST include:
1. **Executive Overview** — A 2-3 sentence high-level summary of the data.
2. **Key Metrics** — Total revenue, units sold, average order value, and any other relevant KPIs.
3. **Top Performers** — Best-performing products, regions, or categories.
4. **Trends & Patterns** — Any notable trends, seasonal patterns, or anomalies.
5. **Actionable Recommendations** — 2-3 strategic recommendations based on the data.

Format the summary in clean, professional prose with clear sections. Use bullet points where
appropriate. The tone should be confident and data-driven, suitable for C-suite executives.
Do NOT include raw data tables — the audience wants insights, not spreadsheets."""


async def generate_sales_summary(data_summary: str) -> str:
    """
    Send the parsed data summary to Gemini and return the AI-generated narrative.

    Args:
        data_summary: Structured text summary of the sales data from the parser.

    Returns:
        A professional narrative summary suitable for executive leadership.
    """
    model = genai.GenerativeModel(settings.gemini_model)

    prompt = f"""Analyze the following sales data and generate a professional executive summary.

--- START OF SALES DATA ---
{data_summary}
--- END OF SALES DATA ---

Generate a comprehensive yet concise executive brief based on this data."""

    response = await model.generate_content_async(prompt)
    return response.text
