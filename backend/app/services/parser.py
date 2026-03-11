"""Service for parsing uploaded CSV/XLSX files into structured text for the LLM."""

import io

import pandas as pd

ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls"}
ALLOWED_CONTENT_TYPES = {
    "text/csv",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-excel",
}


def validate_file_type(filename: str, content_type: str) -> bool:
    """Check if the uploaded file is a supported spreadsheet format."""
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in ALLOWED_EXTENSIONS or content_type in ALLOWED_CONTENT_TYPES


def parse_file_to_dataframe(content: bytes, filename: str) -> pd.DataFrame:
    """Read file bytes into a Pandas DataFrame."""
    if filename.lower().endswith(".csv"):
        return pd.read_csv(io.BytesIO(content))
    else:
        return pd.read_excel(io.BytesIO(content))


def dataframe_to_summary_text(df: pd.DataFrame) -> str:
    """
    Convert a DataFrame into a structured text summary for LLM consumption.
    Includes column info, sample rows, and basic aggregations.
    """
    lines: list[str] = []

    # Basic info
    lines.append(f"Dataset shape: {df.shape[0]} rows × {df.shape[1]} columns")
    lines.append(f"Columns: {', '.join(df.columns.tolist())}")
    lines.append("")

    # Data types
    lines.append("Column data types:")
    for col in df.columns:
        lines.append(f"  - {col}: {df[col].dtype}")
    lines.append("")

    # Sample rows (first 20 or all if fewer)
    sample = df.head(20)
    lines.append(f"Sample data (first {len(sample)} rows):")
    lines.append(sample.to_string(index=False))
    lines.append("")

    # Numeric column statistics
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if numeric_cols:
        lines.append("Numeric column statistics:")
        lines.append(df[numeric_cols].describe().to_string())
        lines.append("")

    # Categorical column value counts
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    if cat_cols:
        lines.append("Categorical column distributions:")
        for col in cat_cols:
            counts = df[col].value_counts().head(10)
            lines.append(f"  {col}:")
            for val, count in counts.items():
                lines.append(f"    - {val}: {count}")
        lines.append("")

    # If there's a Revenue or similar monetary column, add a total
    for col_name in ["Revenue", "revenue", "Total", "total", "Amount", "amount"]:
        if col_name in df.columns:
            lines.append(f"Total {col_name}: {df[col_name].sum():,.2f}")

    return "\n".join(lines)
