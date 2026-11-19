
import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "candidate_resume_dataset.csv"
OUTPUT_PATH = BASE_DIR / "dataset" / "resume_ml_ready.csv"

# Load TSV dataset
df = pd.read_csv(DATA_PATH, sep="\t")

# Select useful input features
feature_columns = [
    "degree_level",
    "degree_field",
    "programming_languages",
    "frameworks_and_tools",
    "ml_and_data_analysis_skills",
    "certifications_mentioned",
    "project_evidence_keywords"
]

# Prepare text features
for column in feature_columns:
    df[column] = df[column].fillna("")

# Combine features into one text field
df["resume_text"] = df[feature_columns].agg(" ".join, axis=1)

# Keep role labels
df["role_labels"] = df["source_resume_category_labels"]

# Remove records with no useful role labels
df = df[
    df["role_labels"].notna()
    & (df["role_labels"].str.strip() != "")
    & (df["role_labels"] != "Unknown")
].copy()

# Save prepared dataset
df[["candidate_id", "resume_text", "role_labels"]].to_csv(
    OUTPUT_PATH, index=False
)

print("Dataset preparation completed!")
print("Records:", len(df))
print("Columns:", ["candidate_id", "resume_text", "role_labels"])
print("Saved to:", OUTPUT_PATH)
