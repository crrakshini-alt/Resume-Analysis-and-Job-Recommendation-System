import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "train.xlsx"

df = pd.read_csv(DATA_PATH, sep="\t")

print("UNIQUE DESIGNATIONS:")
print(df["Designation"].nunique())

print("\nTOP 25 DESIGNATIONS:")
print(df["Designation"].value_counts().head(25))

print("\nGRADUATION YEAR DISTRIBUTION:")
print(df["GraduationYear"].value_counts().sort_index())

print("\nDOJ YEAR DISTRIBUTION:")
print(pd.to_datetime(df["DOJ"], errors="coerce").dt.year.value_counts().sort_index())

print("\nDOL YEAR DISTRIBUTION:")
print(pd.to_datetime(df["DOL"], errors="coerce").dt.year.value_counts().sort_index())

print("\nSALARY CORRELATION WITH ACADEMIC SCORES:")
columns = [
    "Salary",
    "10percentage",
    "12percentage",
    "collegeGPA",
    "English",
    "Logical",
    "Quant",
    "ComputerProgramming"
]

print(df[columns].corr()["Salary"].sort_values(ascending=False))