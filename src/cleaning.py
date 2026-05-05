import pandas as pd
import numpy as np


def load_raw_data(path: str) -> pd.DataFrame:
    """Load and combine both sheets from the UCI Online Retail II dataset."""
    df_1 = pd.read_excel(path, sheet_name="Year 2009-2010")
    df_2 = pd.read_excel(path, sheet_name="Year 2010-2011")
    return pd.concat([df_1, df_2], ignore_index=True)


def cap_outliers(series: pd.Series, lower_q=0.01, upper_q=0.99) -> pd.Series:
    """Winsorize a series at given quantile boundaries."""
    return series.clip(lower=series.quantile(lower_q),
                       upper=series.quantile(upper_q))


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full cleaning pipeline for UCI Online Retail II dataset.
    Steps:
        1. Drop missing Customer IDs
        2. Drop duplicates
        3. Remove cancellations (Invoice starts with C)
        4. Remove invalid quantities and prices
        5. Fix data types
        6. Add Revenue column
        7. Cap outliers via Winsorization
    Returns cleaned DataFrame.
    """
    df = df.copy()

    # Step 1: Drop missing Customer IDs
    df = df.dropna(subset=["Customer ID"])

    # Step 2: Drop duplicates
    df = df.drop_duplicates()

    # Step 3: Remove cancellations
    df = df[~df["Invoice"].astype(str).str.startswith("C")]

    # Step 4: Remove invalid quantities and prices
    df = df[df["Quantity"] > 0]
    df = df[df["Price"] > 0]

    # Step 5: Fix data types
    df["Customer ID"] = df["Customer ID"].astype(int).astype(str)
    df["Invoice"] = df["Invoice"].astype(str)

    # Step 6: Add Revenue column
    df["Revenue"] = df["Quantity"] * df["Price"]

    # Step 7: Cap outliers
    df["Quantity"] = cap_outliers(df["Quantity"])
    df["Price"] = cap_outliers(df["Price"])
    df["Revenue"] = df["Quantity"] * df["Price"]

    return df


if __name__ == "__main__":
    RAW_PATH = "../data/raw/online_retail_II.xlsx"
    OUTPUT_PATH = "../data/processed/clean_retail.csv"

    print("Loading raw data...")
    df_raw = load_raw_data(RAW_PATH)
    print(f"Raw shape: {df_raw.shape}")

    print("Cleaning data...")
    df_clean = clean_data(df_raw)
    print(f"Clean shape: {df_clean.shape}")

    df_clean.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved to {OUTPUT_PATH}")
