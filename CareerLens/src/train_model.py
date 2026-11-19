
import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "placement_data_full_class.csv"

# Load dataset
df = pd.read_csv(DATA_PATH, sep="\t")

# Select input features
features = [
    "ssc_p", "hsc_p", "degree_p", "degree_t",
    "workex", "etest_p", "specialisation", "mba_p"
]

X = df[features]
y = df["status"]

# Separate numerical and categorical columns
numerical_features = [
    "ssc_p", "hsc_p", "degree_p", "etest_p", "mba_p"
]

categorical_features = [
    "degree_t", "workex", "specialisation"
]

# Preprocessing for numerical data
numerical_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="median"))
])

# Preprocessing for categorical data
categorical_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

# Combine preprocessing steps
preprocessor = ColumnTransformer([
    ("num", numerical_transformer, numerical_features),
    ("cat", categorical_transformer, categorical_features)
])

# Create complete ML pipeline
model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000))
])

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Train the model
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
print("\n========== LOGISTIC REGRESSION RESULTS ==========")

print("Accuracy:", accuracy_score(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nModel training completed!")
