
import pandas as pd
import joblib

from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "resume_ml_ready.csv"
MODEL_PATH = BASE_DIR / "models" / "resume_role_model.pkl"

# Load prepared resume dataset
df = pd.read_csv(DATA_PATH)

X = df["resume_text"].fillna("")

# Convert role labels into lists
y_labels = df["role_labels"].fillna("").apply(
    lambda value: [
        role.strip()
        for role in value.split(";")
        if role.strip() and role.strip().lower() != "unknown"
    ]
)
from collections import Counter

role_counts = Counter(
    role
    for labels in y_labels
    for role in labels
)

print("\nROLE-WISE RESUME COUNTS")
for role, count in role_counts.items():
    print(f"{role}: {count}")

print("\nTOTAL UNIQUE ROLES:", len(role_counts))

# Encode multiple job-role labels
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(y_labels)

# Convert resume text into TF-IDF features
vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    sublinear_tf=True,
    stop_words="english"
)

X_vectorized = vectorizer.fit_transform(X)

# Train Logistic Regression model
model = OneVsRestClassifier(
    LogisticRegression(
        C=0.5,
        max_iter=2000,
        class_weight="balanced"
    )
)

model.fit(X_vectorized, y)

# Save model and supporting components together
model_bundle = {
    "model": model,
    "vectorizer": vectorizer,
    "label_encoder": mlb,
    "threshold": 0.5
}

joblib.dump(model_bundle, MODEL_PATH)

print("\nMODEL TRAINING COMPLETED")
print("Training records:", len(df))
print("Number of job roles:", len(mlb.classes_))
print("Job roles:", list(mlb.classes_))
print("Saved model:", MODEL_PATH)
