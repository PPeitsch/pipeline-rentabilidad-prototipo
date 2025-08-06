import pandas as pd
from typing import List

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalizes column names by stripping whitespace, converting to lowercase,
    and replacing non-alphanumeric characters with underscores.
    """
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^A-Za-z0-9_]", "", regex=True)
    )
    return df


def convert_numeric_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Converts specified columns to numeric, coercing errors to NaN.
    It handles non-numeric characters like currency symbols.
    """
    for col in columns:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(r"[^0-9.-]", "", regex=True),
            errors="coerce",
        )
    return df


def standardize_date_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Converts a specified column to datetime objects, inferring the format.
    Errors will be coerced to NaT (Not a Time).
    """
    df[column] = pd.to_datetime(df[column], errors="coerce", format="mixed")
    return df


def strip_string_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Trims leading and trailing whitespace from all string/object columns.
    """
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].str.strip()
    return df


def resolve_sku_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes duplicate records based on 'sku', keeping the one with the
    most recent 'fecha_actualización'.
    """
    df_sorted = df.sort_values("fecha_actualización", ascending=False)
    df_deduplicated = df_sorted.drop_duplicates(subset="sku", keep="first")
    return df_deduplicated


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies a defined strategy for handling missing values:
    - Fills 'categoria' with 'desconocida'.
    - Drops rows where critical columns are null.
    """
    df["categoria"].fillna("desconocida", inplace=True)
    critical_cols = ["precio_compra", "precio_venta", "fecha_actualización"]
    df.dropna(subset=critical_cols, inplace=True)
    return df


def run_cleaning_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Executes the full data cleaning pipeline by calling all cleaning
    functions in the correct sequence.
    """
    print("Starting data cleaning pipeline...")

    df_clean = df.copy()

    # 1. Clean column names
    df_clean = clean_column_names(df_clean)
    print("Step 1/6: Column names normalized.")

    # 2. Convert numeric columns
    numeric_cols = ["precio_venta", "margen"]
    df_clean = convert_numeric_columns(df_clean, numeric_cols)
    print(f"Step 2/6: Converted columns to numeric: {numeric_cols}.")

    # 3. Convert date column
    df_clean = standardize_date_column(df_clean, "fecha_actualización")
    print("Step 3/6: Standardized date column 'fecha_actualización'.")

    # 4. Clean text columns
    df_clean = strip_string_columns(df_clean)
    print("Step 4/6: Stripped whitespace from string columns.")

    # 5. Handle SKU duplicates
    initial_rows = len(df_clean)
    df_clean = resolve_sku_duplicates(df_clean)
    rows_removed = initial_rows - len(df_clean)
    print(f"Step 5/6: Resolved SKU duplicates. Removed {rows_removed} rows.")

    # 6. Handle missing values
    initial_rows = len(df_clean)
    df_clean = handle_missing_values(df_clean)
    rows_removed = initial_rows - len(df_clean)
    print(f"Step 6/6: Handled missing values. Removed {rows_removed} critical null rows.")

    print("\nData cleaning pipeline finished successfully.")
    return df_clean
