
import pandas as pd

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

PREDICTION_PATH = (
    BASE_DIR / "career_datasets" / "role_cv_predictions.csv"
)

READY_PATH = (
    BASE_DIR / "dataset" / "resume_ml_ready.csv"
)

SOURCE_PATH = (
    BASE_DIR / "dataset" / "candidate_resume_dataset.csv"
)

OUTPUT_PATH = (
    BASE_DIR / "career_datasets" / "role_cv_error_cases.csv"
)

# Roles that need investigation first
PRIORITY_ROLES = [
    "Front_End_Developer",
    "Systems_Administrator",
    "Java_Developer",
    "Database_Administrator",
    "Project_manager"
]

# Load data
predictions = pd.read_csv(PREDICTION_PATH)
ready = pd.read_csv(READY_PATH)
source = pd.read_csv(SOURCE_PATH, sep="\t")

# Keep only useful source fields
source_columns = [
    "candidate_id",
    "source_resume_category_labels",
    "programming_languages",
    "frameworks_and_tools",
    "ml_and_data_analysis_skills",
    "project_evidence_keywords",
    "fresher_status"
]

source_columns = [
    col for col in source_columns
    if col in source.columns
]

# Combine prediction, resume and original source information
data = predictions.merge(
    ready[["candidate_id", "resume_text"]],
    on="candidate_id",
    how="left"
)

data = data.merge(
    source[source_columns],
    on="candidate_id",
    how="left"
)

error_records = []

for _, row in data.iterrows():

    actual = set(
        str(row["actual_roles"]).split(";")
    ) - {""}

    predicted = set(
        str(row["predicted_roles"]).split(";")
    ) - {""}

    for role in PRIORITY_ROLES:

        if role in actual and role not in predicted:
            error_type = "False Negative"

        elif role in predicted and role not in actual:
            error_type = "False Positive"

        else:
            continue

        score_column = f"score_{role}"

        error_records.append({
            "candidate_id": row["candidate_id"],
            "role": role,
            "error_type": error_type,
            "actual_roles": row["actual_roles"],
            "predicted_roles": row["predicted_roles"],
            "model_score": row[score_column],
            "source_labels": row.get(
                "source_resume_category_labels", ""
            ),
            "programming_languages": row.get(
                "programming_languages", ""
            ),
            "frameworks_and_tools": row.get(
                "frameworks_and_tools", ""
            ),
            "ml_and_data_analysis_skills": row.get(
                "ml_and_data_analysis_skills", ""
            ),
            "project_evidence_keywords": row.get(
                "project_evidence_keywords", ""
            ),
            "fresher_status": row.get("fresher_status", ""),
            "resume_text": row.get("resume_text", "")
        })

# Create error report
error_report = pd.DataFrame(error_records)

error_report.to_csv(
    OUTPUT_PATH,
    index=False,
    encoding="utf-8-sig"
)

print("\nROLE-WISE ERROR CASE COUNTS")
print("=" * 65)

if not error_report.empty:
    print(
        error_report.groupby(
            ["role", "error_type"]
        ).size().to_string()
    )

    print("\nFIRST TWO EXAMPLES PER ERROR TYPE")
    print("=" * 65)

    for (role, error_type), group in error_report.groupby(
        ["role", "error_type"],
        sort=False
    ):
        print(f"\n{role} | {error_type}")

        for _, row in group.head(2).iterrows():
            print("\nCandidate:", row["candidate_id"])
            print("Model score:", round(row["model_score"], 4))
            print("Original labels:", row["source_labels"])
            print("Programming:", row["programming_languages"])
            print("Frameworks:", row["frameworks_and_tools"])
            print("ML/Data skills:", row["ml_and_data_analysis_skills"])
            print("Projects:", row["project_evidence_keywords"])
            print("Resume:", str(row["resume_text"])[:350])

else:
    print("No error cases found for selected roles.")

print("\nSaved:", OUTPUT_PATH)
print("Total error cases:", len(error_report))
