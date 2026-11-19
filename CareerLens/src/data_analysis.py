
import pandas as pd
from pathlib import Path

# Get the main project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Dataset path
DATA_PATH = BASE_DIR / "dataset" / "candidate_resume_dataset.csv"

# Load the dataset
df = pd.read_csv(DATA_PATH, sep="\t")

# 1. Display basic information
print("\n========== DATASET INFORMATION ==========")

print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])

# 2. Display column names
print("\n========== COLUMN NAMES ==========")

print(df.columns.tolist())

# 3. Display first five records
print("\n========== FIRST FIVE RECORDS ==========")

print(df.head())

# 4. Check missing values
print("\n========== MISSING VALUES ==========")

missing = df.isnull().sum()

print(missing[missing > 0])

# 5. Check missing value percentage
print("\n========== MISSING VALUE PERCENTAGE ==========")

missing_percentage = (df.isnull().mean() * 100).round(2)

print(missing_percentage[missing_percentage > 0])

# 6. Check duplicate records
print("\n========== DUPLICATE RECORDS ==========")

print("Duplicate rows:", df.duplicated().sum())

# 7. Display data types
print("\n========== DATA TYPES ==========")

print(df.dtypes)

# 8. Check hiring outcome
print("\n========== TARGET COLUMN CHECK ==========")

if "hiring_outcome" in df.columns:
    print(df["hiring_outcome"].value_counts(dropna=False))
else:
    print("Hiring outcome column is not available.")

print("\nDataset analysis completed!")
