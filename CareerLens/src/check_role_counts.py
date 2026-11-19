import pandas as pd
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "resume_ml_ready.csv"

df = pd.read_csv(DATA_PATH)

labels = df["role_labels"].fillna("").apply(
    lambda value: [
        role.strip()
        for role in value.split(";")
        if role.strip() and role.strip().lower() != "unknown"
    ]
)

counts = Counter(role for row in labels for role in row)

print("\nROLE-WISE RESUME COUNTS")

for role, count in sorted(counts.items()):
    print(f"{role}: {count}")

print("\nTOTAL UNIQUE ROLES:", len(counts))