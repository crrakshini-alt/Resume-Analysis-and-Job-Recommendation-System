
import pandas as pd

from pathlib import Path

from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
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


# -----------------------------------
# 1. PROJECT PATHS
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "dataset" / "resume_ml_ready.csv"


# -----------------------------------
# 2. LOAD DATASET
# -----------------------------------

df = pd.read_csv(DATA_PATH)

required_columns = ["resume_text", "role_labels"]

if not all(column in df.columns for column in required_columns):
    raise ValueError("Required dataset columns are missing.")

print("Dataset loaded successfully!")
print("Total records:", len(df))


# -----------------------------------
# 3. PREPARE RESUME TEXT
# -----------------------------------

X = df["resume_text"].fillna("").astype(str)


# -----------------------------------
# 4. PREPARE JOB ROLE LABELS
# -----------------------------------

y_labels = df["role_labels"].fillna("").apply(
    lambda value: [
        role.strip()
        for role in value.split(";")
        if role.strip() and role.strip().lower() != "unknown"
    ]
)


# Remove empty resumes and missing labels
valid = X.str.strip().ne("") & y_labels.apply(bool)

X = X[valid].reset_index(drop=True)
y_labels = y_labels[valid].reset_index(drop=True)


# -----------------------------------
# 5. ENCODE MULTIPLE JOB ROLE LABELS
# -----------------------------------

mlb = MultiLabelBinarizer()

y = mlb.fit_transform(y_labels)


# -----------------------------------
# 6. SPLIT TRAINING AND TEST DATA
# -----------------------------------

# Keep identical resume texts in the same split
splitter = GroupShuffleSplit(
    n_splits=1,
    test_size=0.20,
    random_state=42
)

train_index, test_index = next(
    splitter.split(X, y, groups=X)
)

X_train = X.iloc[train_index]
X_test = X.iloc[test_index]

y_train = y[train_index]
y_test = y[test_index]


# Check training examples for every role
for i, role in enumerate(mlb.classes_):

    if len(set(y_train[:, i])) < 2:
        raise ValueError(
            f"Insufficient positive or negative training examples for {role}."
        )


# -----------------------------------
# 7. DISPLAY ROLE DISTRIBUTION
# -----------------------------------

print("\n========== ROLE DISTRIBUTION ==========")

for i, role in enumerate(mlb.classes_):

    train_count = int(y_train[:, i].sum())
    test_count = int(y_test[:, i].sum())

    print(
        f"{role:25} "
        f"Train: {train_count:3} | "
        f"Test: {test_count:3}"
    )


# -----------------------------------
# 8. TF-IDF VECTORIZATION
# -----------------------------------

vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    sublinear_tf=True,
    stop_words="english"
)

X_train_vectorized = vectorizer.fit_transform(X_train)

X_test_vectorized = vectorizer.transform(X_test)


# -----------------------------------
# 9. TRAIN LOGISTIC REGRESSION
# -----------------------------------

model = OneVsRestClassifier(
    LogisticRegression(
        C=0.5,
        max_iter=2000,
        class_weight="balanced"
    )
)

model.fit(X_train_vectorized, y_train)


# -----------------------------------
# 10. PREDICT TEST DATA
# -----------------------------------

probabilities = model.predict_proba(X_test_vectorized)

predictions = (probabilities >= 0.5).astype(int)


# -----------------------------------
# 11. OVERALL MODEL EVALUATION
# -----------------------------------

print("\n========== DATASET DETAILS ==========")

print("Total records:", len(X))
print("Training records:", len(X_train))
print("Testing records:", len(X_test))
print("Total job roles:", len(mlb.classes_))


print("\n========== MODEL EVALUATION ==========")

print(
    "Exact Match Accuracy:",
    round(accuracy_score(y_test, predictions), 4)
)

print(
    "Micro Precision:",
    round(precision_score(
        y_test, predictions,
        average="micro",
        zero_division=0
    ), 4)
)

print(
    "Micro Recall:",
    round(recall_score(
        y_test, predictions,
        average="micro",
        zero_division=0
    ), 4)
)

print(
    "Micro F1 Score:",
    round(f1_score(
        y_test, predictions,
        average="micro",
        zero_division=0
    ), 4)
)

print(
    "Macro F1 Score:",
    round(f1_score(
        y_test, predictions,
        average="macro",
        zero_division=0
    ), 4)
)

print(
    "Hamming Loss:",
    round(hamming_loss(y_test, predictions), 4)
)


# -----------------------------------
# 12. ROLE-WISE CLASSIFICATION REPORT
# -----------------------------------

print("\n========== ROLE-WISE RESULTS ==========")

print(
    classification_report(
        y_test,
        predictions,
        target_names=mlb.classes_,
        zero_division=0
    )
)


# -----------------------------------
# 13. PREDICTED ROLE COUNTS
# -----------------------------------

print("\n========== PREDICTED ROLE COUNTS ==========")

for i, role in enumerate(mlb.classes_):

    actual_count = int(y_test[:, i].sum())
    predicted_count = int(predictions[:, i].sum())

    print(
        f"{role:25} "
        f"Actual: {actual_count:3} | "
        f"Predicted: {predicted_count:3}"
    )


# -----------------------------------
# 14. INCORRECT PREDICTION ANALYSIS
# -----------------------------------

print("\n========== INCORRECT PREDICTIONS ==========")

error_count = 0

for i in range(len(X_test)):

    actual_roles = [
        mlb.classes_[j]
        for j in range(len(mlb.classes_))
        if y_test[i][j] == 1
    ]

    predicted_roles = [
        mlb.classes_[j]
        for j in range(len(mlb.classes_))
        if predictions[i][j] == 1
    ]

    if set(actual_roles) != set(predicted_roles):

        error_count += 1

        print("\nResume:", X_test.iloc[i][:150])

        print("Actual roles:", actual_roles)

        print("Predicted roles:", predicted_roles)


print("\nTotal incorrect resume predictions:", error_count)


# -----------------------------------
# 15. COMPLETION
# -----------------------------------

print("\nEvaluation completed successfully!")
