import pandas as pd

from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_validate, cross_val_predict
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "careercorpus_domain.csv"

df = pd.read_csv(DATA_PATH)

X = df["resume_text"].fillna("")
y = df["domain_label"]

pipeline = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            max_features=10000,
            ngram_range=(1, 2),
            sublinear_tf=True,
            stop_words="english"
        )
    ),
    (
        "classifier",
        LogisticRegression(
            C=1.0,
            max_iter=3000,
            class_weight="balanced"
        )
    )
])

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

print("\nFIVE-FOLD CROSS-VALIDATION")

scores = cross_validate(
    pipeline,
    X,
    y,
    cv=cv,
    scoring=["accuracy", "f1_macro"],
    n_jobs=-1
)

print("Fold accuracies:", scores["test_accuracy"].round(3))
print("Mean accuracy:", round(scores["test_accuracy"].mean(), 4))
print("Mean macro F1:", round(scores["test_f1_macro"].mean(), 4))

print("\nOUT-OF-FOLD CLASSIFICATION REPORT")

predictions = cross_val_predict(
    pipeline,
    X,
    y,
    cv=cv,
    n_jobs=-1
)

print("Overall accuracy:", round(accuracy_score(y, predictions), 4))
print("Macro F1:", round(f1_score(y, predictions, average="macro"), 4))

print("\nCLASSIFICATION REPORT")
print(classification_report(y, predictions, zero_division=0))

print("\nCONFUSION MATRIX")
labels = sorted(y.unique())

matrix = confusion_matrix(y, predictions, labels=labels)

print(pd.DataFrame(
    matrix,
    index=labels,
    columns=labels
).to_string())

print("\nEvaluation completed.")
