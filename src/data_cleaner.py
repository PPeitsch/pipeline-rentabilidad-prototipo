import pandas as pd
from typing import List
from unidecode import unidecode
import re


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalizes column names to be valid Python identifiers.
    Applies unidecode, converts to lowercase, and replaces invalid characters
    with a single underscore.
    """
    cleaned_columns = []
    for col in df.columns:
        # Step 1: Transliterate special characters (e.g., 'ó' -> 'o').
        clean_col = unidecode(str(col))

        # Step 2: Convert to lowercase and replace spaces/hyphens with underscores.
        clean_col = clean_col.strip().lower().replace(" ", "_").replace("-", "_")

        # Step 3: Remove any character that is not a letter, number, or underscore.
        clean_col = re.sub(r"[^\w]", "", clean_col)

        cleaned_columns.append(clean_col)

    df.columns = cleaned_columns
    return df


def convert_numeric_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Converts specified columns to numeric, coercing errors to NaN.
    """
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(r"[^0-9.-]", "", regex=True),
                errors="coerce",
            )
    return df


def standardize_date_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Converts a specified column to datetime objects, inferring the format.
    """
    if column in df.columns:
        df[column] = pd.to_datetime(df[column], errors="coerce", format="mixed")
    return df


def strip_string_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Trims leading and trailing whitespace from all string/object columns.
    """
    string_cols = df.select_dtypes(include=["object"]).columns
    df[string_cols] = df[string_cols].apply(lambda x: x.str.strip())
    return df


def resolve_sku_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes duplicate records based on 'sku', keeping the one with the
    most recent 'fecha_actualizacion'.
    """
    df_sorted = df.sort_values("fecha_actualizacion", ascending=False)
    df_deduplicated = df_sorted.drop_duplicates(subset="sku", keep="first")
    return df_deduplicated


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies a defined strategy for handling missing values.
    """
    # Fix for FutureWarning: use direct assignment instead of chained inplace
    df["categoria"] = df["categoria"].fillna("desconocida")

    critical_cols = ["precio_compra", "precio_venta", "fecha_actualizacion"]
    df.dropna(subset=critical_cols, inplace=True)
    return df


def run_cleaning_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Executes the full data cleaning pipeline by calling all cleaning
    functions in the correct sequence.
    """
    print("Starting data cleaning pipeline...")

    df_clean = df.copy()

    # Step 1: Clean all column names FIRST.
    df_clean = clean_column_names(df_clean)
    print("Step 1/6: Column names normalized.")

    # --- Define the cleaned column names we expect to work with ---
    numeric_cols_to_process = ["precio_venta", "margen"]
    date_col_to_process = "fecha_actualizacion"

    # Step 2: Convert numeric columns
    df_clean = convert_numeric_columns(df_clean, numeric_cols_to_process)
    print(f"Step 2/6: Converted columns to numeric: {numeric_cols_to_process}.")

    # Step 3: Convert date column
    df_clean = standardize_date_column(df_clean, date_col_to_process)
    print(f"Step 3/6: Standardized date column '{date_col_to_process}'.")

    # Step 4: Clean text columns
    df_clean = strip_string_columns(df_clean)
    print("Step 4/6: Stripped whitespace from string columns.")

    # Step 5: Handle SKU duplicates
    initial_rows = len(df_clean)
    df_clean = resolve_sku_duplicates(df_clean)
    rows_removed = initial_rows - len(df_clean)
    print(f"Step 5/6: Resolved SKU duplicates. Removed {rows_removed} rows.")

    # Step 6: Handle missing values
    initial_rows = len(df_clean)
    df_clean = handle_missing_values(df_clean)
    rows_removed = initial_rows - len(df_clean)
    print(
        f"Step 6/6: Handled missing values. Removed {rows_removed} critical null rows."
    )

    print("\nData cleaning pipeline finished successfully.")
    return df_clean
