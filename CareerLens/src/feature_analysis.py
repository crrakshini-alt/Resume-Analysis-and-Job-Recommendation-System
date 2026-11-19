
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "dataset" / "candidate_resume_dataset.csv"

df = pd.read_csv(DATA_PATH, sep="\t")

# Select useful resume-related features
features = [
    "fresher_status",
    "est_work_history_months",
    "degree_level",
    "degree_field",
    "programming_languages",
    "frameworks_and_tools",
    "ml_and_data_analysis_skills",
    "certifications_mentioned",
    "internship_or_intern_role_mentioned",
    "project_evidence_keywords",
    "skills_count"
]

print("\n========== FEATURE ANALYSIS ==========")

for column in features:

    print("\nColumn:", column)

    print("Unique values:", df[column].nunique())

    print("Missing values:", df[column].isnull().sum())

    print("Sample values:")

    print(df[column].dropna().head(5).tolist())

print("\nFeature analysis completed!")
