import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "candidate_resume_dataset.csv"

df = pd.read_csv(DATA_PATH, sep="\t")

experienced = df[
    df["est_work_history_months"] > 36
]

print("\n========== CANDIDATES ABOVE 36 MONTHS ==========")

columns = [
    "candidate_id",
    "fresher_status",
    "est_work_history_months",
    "degree_level",
    "internship_or_intern_role_mentioned"
]

print(experienced[columns].to_string(index=False))

print("\nTotal candidates:", len(experienced))

print("\n========== FRESHER STATUS OF THESE CANDIDATES ==========")
print(experienced["fresher_status"].value_counts())