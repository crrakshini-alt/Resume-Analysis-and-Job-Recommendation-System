import pandas as pd

from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "careercorpus_domain.csv"
OUTPUT_PATH = BASE_DIR / "career_datasets" / "domain_misclassified_oof.csv"

df = pd.read_csv(DATA_PATH)

X = df["resume_text"].fillna("")
y = df["domain_label"]

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        max_features=10000,
        ngram_range=(1, 2),
        sublinear_tf=True,
        stop_words="english"
    )),
    ("classifier", LogisticRegression(
        C=1.0,
        max_iter=3000,
        class_weight="balanced"
    ))
])

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

probabilities = cross_val_predict(
    pipeline,
    X,
    y,
    cv=cv,
    method="predict_proba",
    n_jobs=-1
)

classes = pipeline.fit(X, y).classes_

predicted_indices = probabilities.argmax(axis=1)
predictions = classes[predicted_indices]
confidence = probabilities.max(axis=1)

errors = df.loc[
    predictions != y,
    ["ID", "domain_label", "resume_text"]
].copy()

errors["predicted_domain"] = predictions[predictions != y]
errors["prediction_score"] = confidence[predictions != y].round(4)

errors["actual_domain_score"] = [
    round(probabilities[i, list(classes).index(y.iloc[i])], 4)
    for i in range(len(y)) if predictions[i] != y.iloc[i]
]

errors.to_csv(OUTPUT_PATH, index=False)

print("Total resumes:", len(df))
print("Incorrect predictions:", len(errors))
print("Correct predictions:", len(df) - len(errors))

print("\nERROR PAIRS:")
print(
    errors.groupby(
        ["domain_label", "predicted_domain"]
    ).size().to_string()
)

print("\nFIRST 15 INCORRECT PREDICTIONS:")
for _, row in errors.head(15).iterrows():
    print("\nID:", row["ID"])
    print("Actual:", row["domain_label"])
    print("Predicted:", row["predicted_domain"])
    print("Prediction score:", row["prediction_score"])
    print("Resume:", row["resume_text"][:350])

print("\nSaved error analysis:", OUTPUT_PATH)
