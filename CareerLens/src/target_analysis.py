import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "placement_data_full_class.csv"

df = pd.read_csv(DATA_PATH, sep="\t")

print("\n========== TARGET ANALYSIS ==========")

print("\nPlacement status:")
print(df["status"].value_counts())

print("\nSalary availability by placement status:")
print(
    pd.crosstab(
        df["status"],
        df["salary"].isnull(),
        margins=True
    )
)

print("\nAverage salary by placement status:")
print(df.groupby("status")["salary"].mean())

print("\n========== FEATURE CHECK ==========")

features = [
    "ssc_p",
    "hsc_p",
    "degree_p",
    "degree_t",
    "workex",
    "etest_p",
    "specialisation",
    "mba_p"
]

for column in features:
    print(f"\n{column}")
    print("Unique values:", df[column].nunique())
    print("Missing values:", df[column].isnull().sum())

print("\nTarget analysis completed!")