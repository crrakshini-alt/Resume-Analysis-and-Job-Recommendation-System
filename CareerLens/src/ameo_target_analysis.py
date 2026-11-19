import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "train.xlsx"

df = pd.read_csv(DATA_PATH, sep="\t")

print("Total records:", len(df))

print("\nSalary statistics:")
print(df["Salary"].describe())

print("\nSalary value counts:")
print(df["Salary"].value_counts().head(20))

print("\nNumber of zero salaries:")
print((df["Salary"] == 0).sum())

print("\nDesignation distribution:")
print(df["Designation"].value_counts().head(20))

print("\nDOJ missing or empty:")
print(df["DOJ"].isna().sum())

print("\nDOL missing or empty:")
print(df["DOL"].isna().sum())

print("\nSample employment records:")
print(df[["Salary", "DOJ", "DOL", "Designation"]].head(15))