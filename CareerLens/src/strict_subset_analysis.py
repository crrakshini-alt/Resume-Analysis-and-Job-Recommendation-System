import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "candidate_resume_dataset.csv"

df = pd.read_csv(DATA_PATH, sep="\t")

# Select candidates with estimated work history <= 36 months
strict_subset = df[
    df["est_work_history_months"] <= 36
].copy()

print("\n========== STRICT SUBSET ANALYSIS ==========")

print("Total candidates:", len(strict_subset))

print("\nFresher status distribution:")
print(strict_subset["fresher_status"].value_counts())

print("\nWork experience range:")
print(strict_subset["est_work_history_months"].describe())

print("\nInternship information:")
print(
    strict_subset["internship_or_intern_role_mentioned"]
    .value_counts()
)

print("\nDegree distribution:")
print(strict_subset["degree_level"].value_counts())

print("\nMissing hiring outcomes:")
print(strict_subset["hiring_outcome"].isnull().sum())

print("\nAnalysis completed!")