import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "train.xlsx"
OUTPUT_PATH = BASE_DIR / "dataset" / "ameo_cleaned.csv"

df = pd.read_csv(DATA_PATH, sep="\t")

# Remove unnecessary columns
df = df.drop(columns=["Unnamed: 0", "ID"])

# Convert optional test scores into missing values
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

for col in optional_columns:
    df[col] = df[col].replace(-1, pd.NA)

# Remove the record with invalid graduation year
df = df[df["GraduationYear"] != 0]

# Save cleaned dataset
df.to_csv(OUTPUT_PATH, index=False)

print("Dataset cleaned successfully!")
print("Remaining records:", len(df))
print("Remaining columns:", len(df.columns))
print("Saved to:", OUTPUT_PATH)