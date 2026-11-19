
import pandas as pd
import numpy as np
import joblib

from pathlib import Path
from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    hamming_loss,
    classification_report
)

# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "dataset" / "resume_ml_ready.csv"
MODEL_PATH = BASE_DIR / "models" / "resume_role_model_v2.pkl"

# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------

df = pd.read_csv(DATA_PATH)

X = df["resume_text"].fillna("").astype(str)

y_labels = df["role_labels"].fillna("").apply(
    lambda value: [
        role.strip()
        for role in value.split(";")
        if role.strip() and role.strip().lower() != "unknown"
    ]
)

label_encoder = MultiLabelBinarizer()
y = label_encoder.fit_transform(y_labels)

groups = X.copy()

print("\nCAREERLENS MODEL V2")
print("=" * 60)

print("Total resumes:", len(X))
print("Total job roles:", len(label_encoder.classes_))

print("\nRole distribution:")

role_counts = Counter(
    role
    for labels in y_labels
    for role in labels
)

for role, count in role_counts.items():
    print(f"{role}: {count}")

# --------------------------------------------------
# 3. FEATURE EXTRACTORS
# --------------------------------------------------

def create_word_vectorizer():

    return TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        sublinear_tf=True,
        stop_words="english"
    )


def create_v2_vectorizer():

    return FeatureUnion([
        (
            "word_features",
            TfidfVectorizer(
                max_features=10000,
                ngram_range=(1, 2),
                sublinear_tf=True,
                stop_words="english"
            )
        ),
        (
            "character_features",
            TfidfVectorizer(
                analyzer="char_wb",
                ngram_range=(3, 5),
                max_features=12000,
                min_df=2,
                sublinear_tf=True
            )
        )
    ])


# --------------------------------------------------
# 4. MODEL CREATION
# --------------------------------------------------

def create_model():

    return OneVsRestClassifier(
        LogisticRegression(
            C=0.5,
            max_iter=3000,
            class_weight="balanced"
        )
    )


# --------------------------------------------------
# 5. CROSS-VALIDATION
# --------------------------------------------------

models_to_compare = {
    "Word_Baseline": create_word_vectorizer,
    "Word_Character_V2": create_v2_vectorizer
}

cv = GroupKFold(n_splits=5)

results = {}

for model_name, vectorizer_function in models_to_compare.items():

    print(f"\nEvaluating: {model_name}")
    print("-" * 60)

    oof_predictions = np.zeros_like(y)

    for fold, (train_idx, test_idx) in enumerate(
        cv.split(X, y, groups),
        start=1
    ):

        X_train = X.iloc[train_idx]
        X_test = X.iloc[test_idx]

        y_train = y[train_idx]

        vectorizer = vectorizer_function()

        X_train_vectorized = vectorizer.fit_transform(X_train)
        X_test_vectorized = vectorizer.transform(X_test)

        model = create_model()

        model.fit(X_train_vectorized, y_train)

        probabilities = model.predict_proba(X_test_vectorized)

        predictions = (probabilities >= 0.5).astype(int)

        oof_predictions[test_idx] = predictions

        fold_f1 = f1_score(
            y[test_idx],
            predictions,
            average="micro",
            zero_division=0
        )

        print(f"Fold {fold} micro F1: {fold_f1:.4f}")

    exact_accuracy = accuracy_score(y, oof_predictions)

    micro_f1 = f1_score(
        y,
        oof_predictions,
        average="micro",
        zero_division=0
    )

    macro_f1 = f1_score(
        y,
        oof_predictions,
        average="macro",
        zero_division=0
    )

    hamming = hamming_loss(y, oof_predictions)

    results[model_name] = {
        "exact_accuracy": exact_accuracy,
        "micro_f1": micro_f1,
        "macro_f1": macro_f1,
        "hamming_loss": hamming,
        "predictions": oof_predictions
    }

    print("\nResults:")
    print(f"Exact match accuracy: {exact_accuracy:.4f}")
    print(f"Micro F1:             {micro_f1:.4f}")
    print(f"Macro F1:             {macro_f1:.4f}")
    print(f"Hamming loss:         {hamming:.4f}")

# --------------------------------------------------
# 6. SELECT BEST CANDIDATE
# --------------------------------------------------

print("\n\nMODEL COMPARISON")
print("=" * 60)

for name, result in results.items():

    print(f"\n{name}")
    print(f"Exact accuracy: {result['exact_accuracy']:.4f}")
    print(f"Micro F1:       {result['micro_f1']:.4f}")
    print(f"Macro F1:       {result['macro_f1']:.4f}")
    print(f"Hamming loss:   {result['hamming_loss']:.4f}")

best_name = max(
    results,
    key=lambda name: (
        results[name]["macro_f1"],
        results[name]["micro_f1"]
    )
)

best_result = results[best_name]

print("\nSelected candidate:", best_name)

# --------------------------------------------------
# 7. TRAIN SELECTED MODEL ON ALL DATA
# --------------------------------------------------

if best_name == "Word_Character_V2":
    final_vectorizer = create_v2_vectorizer()
else:
    final_vectorizer = create_word_vectorizer()

X_all_vectorized = final_vectorizer.fit_transform(X)

final_model = create_model()
final_model.fit(X_all_vectorized, y)

# --------------------------------------------------
# 8. SAVE AS A SEPARATE MODEL
# --------------------------------------------------

model_bundle = {
    "model": final_model,
    "vectorizer": final_vectorizer,
    "label_encoder": label_encoder,
    "threshold": 0.5,
    "model_name": best_name,
    "cv_metrics": {
        "exact_accuracy": best_result["exact_accuracy"],
        "micro_f1": best_result["micro_f1"],
        "macro_f1": best_result["macro_f1"],
        "hamming_loss": best_result["hamming_loss"]
    }
}

joblib.dump(model_bundle, MODEL_PATH)

print("\n" + "=" * 60)
print("MODEL V2 TRAINING COMPLETED")
print("=" * 60)

print("Selected model:", best_name)
print("Saved to:", MODEL_PATH)

print("\nFinal cross-validation classification report:")

print(
    classification_report(
        y,
        best_result["predictions"],
        target_names=label_encoder.classes_,
        zero_division=0
    )
)

baseline = results["Word_Baseline"]["macro_f1"]
v2 = results["Word_Character_V2"]["macro_f1"]

print("\nV2 macro F1 improvement over baseline:")
print(f"{v2 - baseline:+.4f}")

if v2 > baseline:
    print("Character features improved macro F1 in this evaluation.")
else:
    print("Character features did not improve macro F1.")
    print("The selected candidate is still saved separately for inspection.")

print("\nExisting model was NOT modified.")
