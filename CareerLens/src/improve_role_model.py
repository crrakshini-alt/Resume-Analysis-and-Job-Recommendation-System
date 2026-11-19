import pandas as pd
import numpy as np
import joblib

from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    hamming_loss
)

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "dataset" / "resume_ml_ready.csv"

MODEL_PATH = (
    BASE_DIR / "models" / "resume_role_model_v3_candidate.pkl"
)

# Previous model's grouped CV results
OLD_MACRO_F1 = 0.4588
OLD_MICRO_F1 = 0.5954

THRESHOLD = 0.5

# --------------------------------------------------
# LOAD EXISTING DATASET
# --------------------------------------------------

df = pd.read_csv(DATA_PATH)

X = df["resume_text"].fillna("").astype(str)

y_labels = df["role_labels"].fillna("").apply(
    lambda value: [
        role.strip()
        for role in value.split(";")
        if role.strip()
        and role.strip().lower() != "unknown"
    ]
)

encoder = MultiLabelBinarizer()
y = encoder.fit_transform(y_labels)

# Group identical resume text to avoid leakage
groups = X.str.strip().str.lower()

cv = GroupKFold(n_splits=5)

# --------------------------------------------------
# EXPERIMENT WITH DIFFERENT C VALUES
# --------------------------------------------------

C_VALUES = [0.1, 0.5, 1.0, 2.0]

results = []

best_macro_f1 = -1
best_micro_f1 = -1
best_C = None

print("\nROLE MODEL IMPROVEMENT EXPERIMENT")
print("=" * 55)

for C in C_VALUES:

    oof_probabilities = np.zeros(
        (len(df), len(encoder.classes_))
    )

    print(f"\nTesting Logistic Regression C = {C}")

    for train_idx, test_idx in cv.split(X, y, groups):

        X_train = X.iloc[train_idx]
        X_test = X.iloc[test_idx]

        y_train = y[train_idx]

        vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            sublinear_tf=True,
            stop_words="english"
        )

        X_train_vectorized = vectorizer.fit_transform(X_train)
        X_test_vectorized = vectorizer.transform(X_test)

        model = OneVsRestClassifier(
            LogisticRegression(
                C=C,
                max_iter=2000,
                class_weight="balanced"
            )
        )

        model.fit(X_train_vectorized, y_train)

        probabilities = model.predict_proba(
            X_test_vectorized
        )

        oof_probabilities[test_idx] = probabilities

    predictions = (
        oof_probabilities >= THRESHOLD
    ).astype(int)

    exact_accuracy = accuracy_score(y, predictions)

    micro_f1 = f1_score(
        y, predictions,
        average="micro",
        zero_division=0
    )

    macro_f1 = f1_score(
        y, predictions,
        average="macro",
        zero_division=0
    )

    loss = hamming_loss(y, predictions)

    results.append({
        "C": C,
        "exact_accuracy": exact_accuracy,
        "micro_f1": micro_f1,
        "macro_f1": macro_f1,
        "hamming_loss": loss
    })

    print(f"Exact accuracy : {exact_accuracy:.4f}")
    print(f"Micro F1       : {micro_f1:.4f}")
    print(f"Macro F1       : {macro_f1:.4f}")
    print(f"Hamming loss   : {loss:.4f}")

    if (
        macro_f1 > best_macro_f1
        or (
            macro_f1 == best_macro_f1
            and micro_f1 > best_micro_f1
        )
    ):
        best_macro_f1 = macro_f1
        best_micro_f1 = micro_f1
        best_C = C

# --------------------------------------------------
# TRAIN BEST CANDIDATE ON ALL EXISTING DATA
# --------------------------------------------------

print("\n" + "=" * 55)
print("BEST CONFIGURATION")
print("C:", best_C)
print("Macro F1:", round(best_macro_f1, 4))
print("Micro F1:", round(best_micro_f1, 4))

vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    sublinear_tf=True,
    stop_words="english"
)

X_vectorized = vectorizer.fit_transform(X)

final_model = OneVsRestClassifier(
    LogisticRegression(
        C=best_C,
        max_iter=2000,
        class_weight="balanced"
    )
)

final_model.fit(X_vectorized, y)

# Keep the same bundle format used by predict_roles.py
model_bundle = {
    "model": final_model,
    "vectorizer": vectorizer,
    "label_encoder": encoder,
    "threshold": THRESHOLD,
    "evaluation": {
        "C": best_C,
        "macro_f1": best_macro_f1,
        "micro_f1": best_micro_f1,
        "previous_macro_f1": OLD_MACRO_F1,
        "previous_micro_f1": OLD_MICRO_F1,
        "improved_over_previous": (
            best_macro_f1 > OLD_MACRO_F1
            and best_micro_f1 >= OLD_MICRO_F1
        )
    }
}

MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

joblib.dump(model_bundle, MODEL_PATH)

print("\nCANDIDATE MODEL SAVED")
print(MODEL_PATH)

if (
    best_macro_f1 > OLD_MACRO_F1
    and best_micro_f1 >= OLD_MICRO_F1
):
    print("\nCandidate improved over the previous reported baseline.")
else:
    print("\nNo proven improvement over the previous baseline.")
    print("Keep using the original model.")

print("\nOriginal model was NOT modified.")