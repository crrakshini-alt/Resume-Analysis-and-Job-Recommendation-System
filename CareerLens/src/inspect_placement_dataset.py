import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR / "dataset" / "placement_data_full_class.csv"
)

df = pd.read_csv(DATA_PATH, sep="\t")

print("\n========== DATASET INFORMATION ==========")

print("Number of records:", len(df))
print("Number of columns:", len(df.columns))

print("\n========== COLUMN NAMES ==========")
print(df.columns.tolist())

print("\n========== FIRST FIVE RECORDS ==========")
print(df.head())

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

print("\n========== DUPLICATE RECORDS ==========")
print("Duplicate rows:", df.duplicated().sum())

print("\n========== PLACEMENT STATUS ==========")
print(df["status"].value_counts())

print("\n========== PLACEMENT STATUS PERCENTAGE ==========")
print(df["status"].value_counts(normalize=True) * 100)

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\nDataset inspection completed!")