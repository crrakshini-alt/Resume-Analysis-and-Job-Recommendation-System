import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "train.xlsx"

df = pd.read_csv(DATA_PATH, sep="\t")

optional_columns = [
    "Domain",
    "ComputerProgramming",
    "ElectronicsAndSemicon",
    "ComputerScience",
    "MechanicalEngg",
    "ElectricalEngg",
    "TelecomEngg",
    "CivilEngg"
]

print("OPTIONAL TEST SCORES (-1 VALUES)")
print("--------------------------------")

for col in optional_columns:
    print(col, ":", (df[col] == -1).sum())

print("\nSALARY DISTRIBUTION")
print("-------------------")
print(df["Salary"].describe())

print("\nINVALID OR UNUSUAL VALUES")
print("-------------------------")
print("Graduation year 0:", (df["GraduationYear"] == 0).sum())
print("Salary <= 0:", (df["Salary"] <= 0).sum())

print("\nDUPLICATE CANDIDATE IDs")
print(df["ID"].duplicated().sum())

print("\nDUPLICATE ROWS")
print(df.duplicated().sum())