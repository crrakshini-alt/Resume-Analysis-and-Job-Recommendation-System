import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "candidate_resume_dataset.csv"

df = pd.read_csv(DATA_PATH, sep="\t")

print("\n========== WORK EXPERIENCE ==========")
print(df["est_work_history_months"].describe())

print("\n========== FRESHER STATUS ==========")
print(df["fresher_status"].value_counts())

print("\n========== INTERNSHIP INFORMATION ==========")
print(df["internship_or_intern_role_mentioned"].value_counts())

print("\n========== DEGREE LEVEL ==========")
print(df["degree_level"].value_counts())

print("\n========== WORK HISTORY GROUPS ==========")

conditions = [
    df["est_work_history_months"].between(0, 12),
    df["est_work_history_months"].between(13, 36),
    df["est_work_history_months"] > 36
]

labels = [
    "0-12 months",
    "13-36 months",
    "Above 36 months"
]

df["work_experience_group"] = pd.Series(
    pd.NA, index=df.index, dtype="object"
)

import numpy as np

df["work_experience_group"] = np.select(
    conditions,
    labels,
    default="Other or invalid"
)

print(df["work_experience_group"].value_counts())

print("\n========== DATA QUALITY CHECK ==========")
print("Total records:", len(df))
print("Unique candidate IDs:", df["candidate_id"].nunique())
print("Missing candidate IDs:", df["candidate_id"].isnull().sum())

print("\nData quality check completed!")