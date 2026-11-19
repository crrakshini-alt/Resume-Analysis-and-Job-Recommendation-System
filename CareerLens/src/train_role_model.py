
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import KFold, train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    f1_score,
    classification_report
)


# --------------------------------------------------
# 1. LOAD DATASET
# --------------------------------------------------

df = pd.read_csv("dataset/resume_ml_ready.csv")

print("Total resumes:", len(df))

# Extract resume text
X = df["resume_text"].fillna("")

# Convert semicolon-separated roles into lists
y_labels = df["role_labels"].fillna("").apply(
    lambda x: [
        role.strip()
        for role in x.split(";")
        if role.strip() and role.strip().lower() != "unknown"
    ]
)

# Convert labels into binary format
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(y_labels)

print("Number of job roles:", len(mlb.classes_))
print("Job roles:", list(mlb.classes_))


# --------------------------------------------------
# 2. DEFINE MODELS
# --------------------------------------------------

models = {
    "Logistic Regression": OneVsRestClassifier(
        LogisticRegression(
            C=0.5,
            max_iter=2000,
            class_weight="balanced"
        )
    ),

    "Linear SVM": OneVsRestClassifier(
        LinearSVC(
            C=0.5,
            class_weight="balanced",
            max_iter=5000
        )
    ),

    "Random Forest": OneVsRestClassifier(
        RandomForestClassifier(
            n_estimators=200,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1
        )
    )
}


# --------------------------------------------------
# 3. THRESHOLD TUNING
# --------------------------------------------------

def find_best_threshold(y_true, scores, model_name):

    if model_name == "Linear SVM":
        thresholds = np.arange(-1.0, 1.01, 0.1)
    else:
        thresholds = np.arange(0.20, 0.71, 0.05)

    best_threshold = thresholds[0]
    best_score = -1

    for threshold in thresholds:

        predictions = (scores >= threshold).astype(int)

        score = f1_score(
            y_true,
            predictions,
            average="micro",
            zero_division=0
        )

        if score > best_score:
            best_score = score
            best_threshold = threshold

    return best_threshold


# --------------------------------------------------
# 4. CROSS-VALIDATION
# --------------------------------------------------

kf = KFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

model_results = {}

for model_name, model in models.items():

    print("\n" + "=" * 65)
    print("TRAINING:", model_name)
    print("=" * 65)

    fold_scores = []

    # Store predictions at their original dataset positions
    oof_predictions = np.zeros_like(y)

    for fold, (train_index, test_index) in enumerate(
        kf.split(X), start=1
    ):

        X_train = X.iloc[train_index]
        X_test = X.iloc[test_index]

        y_train = y[train_index]
        y_test = y[test_index]

        # Validation split for threshold selection
        X_fit, X_val, y_fit, y_val = train_test_split(
            X_train,
            y_train,
            test_size=0.20,
            random_state=42
        )

        # Create TF-IDF features
        vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            sublinear_tf=True,
            stop_words="english"
        )

        X_fit_tfidf = vectorizer.fit_transform(X_fit)
        X_val_tfidf = vectorizer.transform(X_val)

        # Train model on training portion
        model.fit(X_fit_tfidf, y_fit)

        # Get validation scores
        if model_name == "Linear SVM":
            val_scores = model.decision_function(X_val_tfidf)
        else:
            val_scores = model.predict_proba(X_val_tfidf)

        # Find threshold using validation data only
        threshold = find_best_threshold(
            y_val,
            val_scores,
            model_name
        )

        # Retrain using the complete training fold
        X_train_tfidf = vectorizer.fit_transform(X_train)
        X_test_tfidf = vectorizer.transform(X_test)

        model.fit(X_train_tfidf, y_train)

        # Predict on unseen test fold
        if model_name == "Linear SVM":
            test_scores = model.decision_function(X_test_tfidf)
        else:
            test_scores = model.predict_proba(X_test_tfidf)

        test_predictions = (
            test_scores >= threshold
        ).astype(int)

        # Store predictions in original dataset positions
        oof_predictions[test_index] = test_predictions

        # Calculate fold Micro F1
        fold_f1 = f1_score(
            y_test,
            test_predictions,
            average="micro",
            zero_division=0
        )

        fold_scores.append(fold_f1)

        print(
            f"Fold {fold} | "
            f"Threshold: {threshold:.2f} | "
            f"Micro F1: {fold_f1:.4f}"
        )

    # Calculate overall metrics
    all_true = y
    all_predictions = oof_predictions

    micro_f1 = f1_score(
        all_true,
        all_predictions,
        average="micro",
        zero_division=0
    )

    macro_f1 = f1_score(
        all_true,
        all_predictions,
        average="macro",
        zero_division=0
    )

    model_results[model_name] = {
        "micro_f1": micro_f1,
        "macro_f1": macro_f1,
        "mean_fold_f1": np.mean(fold_scores),
        "true": all_true,
        "predictions": all_predictions
    }

    print("\nClassification Report:")
    print(
        classification_report(
            all_true,
            all_predictions,
            target_names=mlb.classes_,
            zero_division=0
        )
    )


# --------------------------------------------------
# 5. FINAL MODEL COMPARISON
# --------------------------------------------------

print("\n" + "=" * 75)
print("FINAL MODEL COMPARISON")
print("=" * 75)

comparison = []

for model_name, result in model_results.items():

    comparison.append({
        "Model": model_name,
        "Mean Fold Micro F1": result["mean_fold_f1"],
        "Overall Micro F1": result["micro_f1"],
        "Macro F1": result["macro_f1"]
    })

comparison_df = pd.DataFrame(comparison)

print(
    comparison_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)


# --------------------------------------------------
# 6. SELECT CURRENT LEADING MODEL
# --------------------------------------------------

best_model_name = max(
    model_results,
    key=lambda name: model_results[name]["micro_f1"]
)

print("\nCurrent leading model:", best_model_name)


# --------------------------------------------------
# 7. LOGISTIC REGRESSION ERROR ANALYSIS
# --------------------------------------------------

print("\n" + "=" * 75)
print("ERROR ANALYSIS: LOGISTIC REGRESSION")
print("=" * 75)

lr_results = model_results["Logistic Regression"]

actual = lr_results["true"]
predicted = lr_results["predictions"]


# --------------------------------------------------
# 8. ROLE-WISE ERROR COUNTS
# --------------------------------------------------

print("\nROLE-WISE ERROR COUNTS")
print("-" * 65)

for index, role in enumerate(mlb.classes_):

    true_positive = np.sum(
        (actual[:, index] == 1) &
        (predicted[:, index] == 1)
    )

    false_positive = np.sum(
        (actual[:, index] == 0) &
        (predicted[:, index] == 1)
    )

    false_negative = np.sum(
        (actual[:, index] == 1) &
        (predicted[:, index] == 0)
    )

    print(f"\nRole: {role}")
    print("Correctly predicted:", true_positive)
    print("Incorrect extra predictions:", false_positive)
    print("Missed predictions:", false_negative)


# --------------------------------------------------
# 9. INCORRECTLY CLASSIFIED RESUMES
# --------------------------------------------------

print("\n\nINCORRECTLY CLASSIFIED RESUMES")
print("-" * 65)

candidate_ids = df["candidate_id"].values

error_count = 0

for i in range(len(actual)):

    actual_roles = [
        mlb.classes_[j]
        for j in range(len(mlb.classes_))
        if actual[i, j] == 1
    ]

    predicted_roles = [
        mlb.classes_[j]
        for j in range(len(mlb.classes_))
        if predicted[i, j] == 1
    ]

    if set(actual_roles) != set(predicted_roles):

        error_count += 1

        if error_count <= 10:

            print("\nCandidate ID:", candidate_ids[i])
            print("Actual roles:", actual_roles)
            print("Predicted roles:", predicted_roles)

print("\nTotal incorrectly classified resumes:", error_count)
print("Displayed first 10 incorrect examples.")


# --------------------------------------------------
# 10. FINAL SUMMARY
# --------------------------------------------------

print("\n" + "=" * 65)
print("EXPERIMENT COMPLETED")
print("=" * 65)

print("Leading model:", best_model_name)
print(
    "Micro F1:",
    round(model_results[best_model_name]["micro_f1"], 4)
)
print(
    "Macro F1:",
    round(model_results[best_model_name]["macro_f1"], 4)
)

print("\nError analysis completed.")
