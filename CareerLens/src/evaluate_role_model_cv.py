
import pandas as pd

from pathlib import Path
from sklearn.model_selection import GroupKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    hamming_loss,
    classification_report
)

# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "dataset" / "resume_ml_ready.csv"
OUTPUT_DIR = BASE_DIR / "career_datasets"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. Load dataset
# --------------------------------------------------

df = pd.read_csv(DATA_PATH)

X = df["resume_text"].fillna("")

y_labels = df["role_labels"].fillna("").apply(
    lambda value: [
        role.strip()
        for role in value.split(";")
        if role.strip() and role.strip().lower() != "unknown"
    ]
)

# Convert multi-label roles into binary format
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(y_labels)

# Group identical resume texts to prevent data leakage
groups = X.copy()

cv = GroupKFold(n_splits=5)

# --------------------------------------------------
# 3. Store out-of-fold predictions and scores
# --------------------------------------------------

oof_predictions = pd.DataFrame(
    0,
    index=range(len(df)),
    columns=range(len(mlb.classes_))
)

oof_scores = pd.DataFrame(
    0.0,
    index=range(len(df)),
    columns=range(len(mlb.classes_))
)

# --------------------------------------------------
# 4. Five-fold cross-validation
# --------------------------------------------------

for fold, (train_idx, test_idx) in enumerate(
    cv.split(X, y, groups),
    start=1
):
    print(f"\nTraining fold {fold}/5...")

    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        sublinear_tf=True,
        stop_words="english"
    )

    X_train = vectorizer.fit_transform(X.iloc[train_idx])
    X_test = vectorizer.transform(X.iloc[test_idx])

    model = OneVsRestClassifier(
        LogisticRegression(
            C=0.5,
            max_iter=2000,
            class_weight="balanced"
        )
    )

    model.fit(X_train, y[train_idx])

    scores = model.predict_proba(X_test)

    predictions = (scores >= 0.5).astype(int)

    oof_predictions.iloc[test_idx] = predictions
    oof_scores.iloc[test_idx] = scores

# --------------------------------------------------
# 5. Overall evaluation
# --------------------------------------------------

y_pred = oof_predictions.values

print("\n" + "=" * 65)
print("5-FOLD GROUP CROSS-VALIDATION RESULTS")
print("=" * 65)

print("Candidates:", len(df))
print("Roles:", len(mlb.classes_))

print(
    "Exact match accuracy:",
    round(accuracy_score(y, y_pred), 4)
)

print(
    "Micro precision:",
    round(
        precision_score(y, y_pred, average="micro", zero_division=0),
        4
    )
)

print(
    "Micro recall:",
    round(
        recall_score(y, y_pred, average="micro", zero_division=0),
        4
    )
)

print(
    "Micro F1:",
    round(
        f1_score(y, y_pred, average="micro", zero_division=0),
        4
    )
)

print(
    "Macro F1:",
    round(
        f1_score(y, y_pred, average="macro", zero_division=0),
        4
    )
)

print(
    "Hamming loss:",
    round(hamming_loss(y, y_pred), 4)
)

print("\nROLE-WISE CLASSIFICATION REPORT")

print(
    classification_report(
        y,
        y_pred,
        target_names=mlb.classes_,
        zero_division=0
    )
)

# --------------------------------------------------
# 6. Candidate-level prediction report
# --------------------------------------------------

actual_roles = mlb.inverse_transform(y)
predicted_roles = mlb.inverse_transform(y_pred)

prediction_report = pd.DataFrame({
    "candidate_id": df["candidate_id"],
    "actual_roles": [";".join(roles) for roles in actual_roles],
    "predicted_roles": [";".join(roles) for roles in predicted_roles],
    "exact_match": [
        set(actual) == set(predicted)
        for actual, predicted in zip(
            actual_roles,
            predicted_roles
        )
    ]
})

score_report = pd.DataFrame(
    oof_scores.values,
    columns=[
        f"score_{role}"
        for role in mlb.classes_
    ]
)

prediction_report = pd.concat(
    [prediction_report, score_report],
    axis=1
)

prediction_path = OUTPUT_DIR / "role_cv_predictions.csv"

prediction_report.to_csv(
    prediction_path,
    index=False,
    encoding="utf-8-sig"
)

# --------------------------------------------------
# 7. Role-wise error analysis
# --------------------------------------------------

error_records = []

for index, role in enumerate(mlb.classes_):

    actual = y[:, index]
    predicted = y_pred[:, index]

    error_records.append({
        "role": role,
        "actual_positive": int(actual.sum()),
        "predicted_positive": int(predicted.sum()),
        "true_positive": int(
            ((actual == 1) & (predicted == 1)).sum()
        ),
        "false_positive": int(
            ((actual == 0) & (predicted == 1)).sum()
        ),
        "false_negative": int(
            ((actual == 1) & (predicted == 0)).sum()
        )
    })

error_report = pd.DataFrame(error_records)

error_path = OUTPUT_DIR / "role_cv_error_summary.csv"

error_report.to_csv(
    error_path,
    index=False,
    encoding="utf-8-sig"
)

# --------------------------------------------------
# 8. Display and save results
# --------------------------------------------------

print("\nROLE-WISE ERROR SUMMARY")
print("=" * 65)

print(error_report.to_string(index=False))

print("\nEXACT MATCH SUMMARY")
print(
    prediction_report["exact_match"]
    .value_counts()
    .rename(index={True: "Correct", False: "Incorrect"})
    .to_string()
)

print("\nEvaluation completed successfully!")

print("\nGenerated files:")
print(prediction_path)
print(error_path)
