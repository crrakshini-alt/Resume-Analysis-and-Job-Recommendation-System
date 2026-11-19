import pandas as pd
from pathlib import Path

from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    cross_validate
)

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    make_scorer
)

# Load dataset
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "placement_data_full_class.csv"

df = pd.read_csv(DATA_PATH, sep="\t")

# Select features and target
features = [
    "ssc_p", "hsc_p", "degree_p", "degree_t",
    "workex", "etest_p", "specialisation", "mba_p"
]

X = df[features]
y = df["status"]

numerical_features = [
    "ssc_p", "hsc_p", "degree_p", "etest_p", "mba_p"
]

categorical_features = [
    "degree_t", "workex", "specialisation"
]

# Preprocessing
preprocessor = ColumnTransformer([
    ("num", SimpleImputer(strategy="median"), numerical_features),
    ("cat", Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ]), categorical_features)
])

# Define models
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )
}

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Five-fold stratified cross-validation
cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

scoring = {
    "accuracy": "accuracy",
    "precision": make_scorer(
        precision_score,
        pos_label="Placed",
        zero_division=0
    ),
    "recall": make_scorer(
        recall_score,
        pos_label="Placed",
        zero_division=0
    ),
    "f1": make_scorer(
        f1_score,
        pos_label="Placed",
        zero_division=0
    )
}

results = []

# Train and evaluate models
for name, classifier in models.items():

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", classifier)
    ])

    # Cross-validation on training data
    cv_results = cross_validate(
        model,
        X_train,
        y_train,
        cv=cv,
        scoring=scoring
    )

    # Train on complete training data
    model.fit(X_train, y_train)

    # Test on unseen data
    predictions = model.predict(X_test)

    results.append({
        "Model": name,

        "CV Accuracy": round(
            cv_results["test_accuracy"].mean(), 4
        ),

        "CV Precision": round(
            cv_results["test_precision"].mean(), 4
        ),

        "CV Recall": round(
            cv_results["test_recall"].mean(), 4
        ),

        "CV F1": round(
            cv_results["test_f1"].mean(), 4
        ),

        "Test Accuracy": round(
            accuracy_score(y_test, predictions), 4
        ),

        "Test F1": round(
            f1_score(
                y_test,
                predictions,
                pos_label="Placed",
                zero_division=0
            ), 4
        )
    })

# Display comparison
comparison = pd.DataFrame(results)

print("\n========== MODEL COMPARISON ==========")
print(comparison.to_string(index=False))

print("\nCross-validation and model comparison completed!")