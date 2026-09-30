"""
Reusable CSV analysis functions for VEDA Technology Task 30.
Uses only Python standard library + pandas.
"""

from __future__ import annotations
import pandas as pd


class DataAnalysisError(Exception):
    """Raised for user-friendly data analysis errors."""


def load_csv(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise DataAnalysisError(f"CSV file not found: {file_path}")
    except Exception as exc:
        raise DataAnalysisError(f"Could not read CSV: {exc}")

    if df.empty:
        raise DataAnalysisError("The CSV file is empty.")
    return df


def validate_columns(df: pd.DataFrame, columns: list[str]) -> None:
    missing = [c for c in columns if c not in df.columns]
    if missing:
        raise DataAnalysisError(
            "Missing column(s): " + ", ".join(missing) +
            ". Available columns: " + ", ".join(map(str, df.columns))
        )


def summary(df: pd.DataFrame) -> dict:
    numeric = df.select_dtypes(include="number")
    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "column_names": [str(c) for c in df.columns],
        "missing_values": int(df.isna().sum().sum()),
        "numeric_columns": [str(c) for c in numeric.columns],
    }


def filter_data(df: pd.DataFrame, column: str, value: str) -> pd.DataFrame:
    validate_columns(df, [column])
    series = df[column].astype(str)
    # Case-insensitive exact match first; if no exact match, substring match.
    exact = df[series.str.lower() == str(value).lower()]
    if not exact.empty:
        return exact
    return df[series.str.contains(str(value), case=False, na=False)]


def group_data(df: pd.DataFrame, column: str, metric: str | None = None) -> pd.DataFrame:
    validate_columns(df, [column])
    if metric:
        validate_columns(df, [metric])
        if not pd.api.types.is_numeric_dtype(df[metric]):
            raise DataAnalysisError(f"Metric column '{metric}' must be numeric.")
        result = df.groupby(column, dropna=False)[metric].agg(
            ["count", "sum", "mean", "min", "max"]
        ).reset_index()
        return result.sort_values("sum", ascending=False)
    result = df.groupby(column, dropna=False).size().reset_index(name="count")
    return result.sort_values("count", ascending=False)


def statistics(df: pd.DataFrame, column: str) -> dict:
    validate_columns(df, [column])
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise DataAnalysisError(f"Column '{column}' must be numeric.")
    s = df[column].dropna()
    if s.empty:
        raise DataAnalysisError(f"Column '{column}' contains no numeric values.")
    return {
        "count": int(s.count()),
        "mean": float(s.mean()),
        "median": float(s.median()),
        "min": float(s.min()),
        "max": float(s.max()),
        "std": float(s.std()) if len(s) > 1 else 0.0,
        "sum": float(s.sum()),
    }


def preview(df: pd.DataFrame, rows: int = 10) -> list[dict]:
    return df.head(max(1, min(rows, 50))).where(pd.notna(df), None).to_dict("records")
