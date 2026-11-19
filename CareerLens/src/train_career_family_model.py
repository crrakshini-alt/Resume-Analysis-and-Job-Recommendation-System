
import pandas as pd
import numpy as np
import joblib

from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report
)

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR
    / "career_datasets"
    / "external_raw"
    / "clean_resume_data.csv"
)

CLEAN_PATH = (
    BASE_DIR
    / "career_datasets"
    / "external_raw"
    / "career_family_clean.csv"
)

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "career_family_model.pkl"
)

# --------------------------------------------------
# 1. LOAD AND CLEAN DATA
# --------------------------------------------------

df = pd.read_csv(DATA_PATH)

df = df[["ID", "Category", "Feature"]].copy()

df["Feature"] = df["Feature"].fillna("").astype(str).str.strip()
df["Category"] = df["Category"].astype(str).str.strip().str.upper()

# Remove records with empty resume text or category.
df = df[
    (df["Feature"] != "")
    & (df["Category"] != "")
].copy()

print("\nINITIAL DATA")
print("=" * 55)
print("Valid records:", len(df))

# --------------------------------------------------
# 2. HANDLE DUPLICATE RESUME TEXT
# --------------------------------------------------

label_counts = df.groupby("Feature")["Category"].nunique()

conflicting_texts = label_counts[label_counts > 1].index

conflict_rows = df[
    df["Feature"].isin(conflicting_texts)
]

print("\nDUPLICATE ANALYSIS")
print("=" * 55)

print("Conflicting resume texts:", len(conflicting_texts))
print("Rows with conflicting labels:", len(conflict_rows))

if len(conflict_rows):
    print("\nConflicting records:")
    print(
        conflict_rows[
            ["ID", "Category"]
        ].to_string(index=False)
    )

# Exclude conflicting duplicate groups rather than
# arbitrarily choosing one of their labels.
df = df[
    ~df["Feature"].isin(conflicting_texts)
].copy()

before = len(df)

df = df.drop_duplicates(
    subset="Feature",
    keep="first"
).copy()

print("Same-label duplicate rows removed:", before - len(df))

# --------------------------------------------------
# 3. SAVE CLEANED DATA SEPARATELY
# --------------------------------------------------

df.to_csv(CLEAN_PATH, index=False)

X = df["Feature"]
y = df["Category"]

print("\nCLEAN DATA SUMMARY")
print("=" * 55)

print("Total resumes:", len(df))
print("Total categories:", y.nunique())

print("\nCategory distribution:")
print(y.value_counts().to_string())

print("\nSaved cleaned dataset:", CLEAN_PATH)

# --------------------------------------------------
# 4. MODEL DEFINITIONS
# --------------------------------------------------

def create_pipeline(classifier):

    return Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                max_features=20000,
                ngram_range=(1, 2),
                sublinear_tf=True,
                stop_words="english",
                min_df=2
            )
        ),
        ("classifier", classifier)
    ])


models = {
    "Logistic_Regression": create_pipeline(
        LogisticRegression(
            C=1.0,
            max_iter=3000,
            class_weight="balanced"
        )
    ),

    "Linear_SVM": create_pipeline(
        LinearSVC(
            C=1.0,
            class_weight="balanced"
        )
    )
}

# --------------------------------------------------
# 5. STRATIFIED CROSS-VALIDATION
# --------------------------------------------------

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

results = {}

print("\nMODEL EVALUATION")
print("=" * 55)

for name, pipeline in models.items():

    print(f"\nEvaluating {name}...")

    predictions = cross_val_predict(
        pipeline,
        X,
        y,
        cv=cv,
        n_jobs=-1
    )

    accuracy = accuracy_score(y, predictions)

    macro_f1 = f1_score(
        y,
        predictions,
        average="macro"
    )

    weighted_f1 = f1_score(
        y,
        predictions,
        average="weighted"
    )

    results[name] = {
        "accuracy": accuracy,
        "macro_f1": macro_f1,
        "weighted_f1": weighted_f1,
        "predictions": predictions
    }

    print(f"Accuracy:    {accuracy:.4f}")
    print(f"Macro F1:    {macro_f1:.4f}")
    print(f"Weighted F1: {weighted_f1:.4f}")

# --------------------------------------------------
# 6. SELECT MODEL USING MACRO F1
# --------------------------------------------------

best_name = max(
    results,
    key=lambda name: (
        results[name]["macro_f1"],
        results[name]["accuracy"]
    )
)

best_result = results[best_name]

print("\nMODEL COMPARISON")
print("=" * 55)

for name, result in results.items():

    print(f"\n{name}")
    print("Accuracy:", round(result["accuracy"], 4))
    print("Macro F1:", round(result["macro_f1"], 4))
    print("Weighted F1:", round(result["weighted_f1"], 4))

print("\nSelected model:", best_name)

# --------------------------------------------------
# 7. FINAL TRAINING
# --------------------------------------------------

final_model = models[best_name]

final_model.fit(X, y)

# --------------------------------------------------
# 8. SAVE SEPARATELY
# --------------------------------------------------

model_bundle = {
    "model": final_model,
    "model_name": best_name,
    "categories": sorted(y.unique()),
    "evaluation": {
        "accuracy": best_result["accuracy"],
        "macro_f1": best_result["macro_f1"],
        "weighted_f1": best_result["weighted_f1"]
    }
}

joblib.dump(model_bundle, MODEL_PATH)

# --------------------------------------------------
# 9. CLASSIFICATION REPORT
# --------------------------------------------------

print("\nCLASSIFICATION REPORT")
print("=" * 55)

print(
    classification_report(
        y,
        best_result["predictions"],
        zero_division=0
    )
)

print("\nTRAINING COMPLETED")
print("=" * 55)

print("Selected model:", best_name)
print("Saved model:", MODEL_PATH)

print("\nOriginal resume dataset preserved.")
print("Original 10-role model preserved.")
