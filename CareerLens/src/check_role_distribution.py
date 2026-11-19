
import pandas as pd
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "resume_ml_ready.csv"

df = pd.read_csv(DATA_PATH)

role_counts = Counter()

for labels in df["role_labels"]:
    roles = [
        role.strip()
        for role in labels.split(";")
        if role.strip() and role.strip() != "Unknown"
    ]
    role_counts.update(roles)

print("JOB ROLE DISTRIBUTION")
print("---------------------")

for role, count in role_counts.most_common():
    print(f"{role}: {count}")

print("\nTotal resumes:", len(df))
print("Total role labels:", sum(role_counts.values()))
