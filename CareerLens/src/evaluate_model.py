import pandas as pd
import joblib

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "placement_data_full_class.csv"
MODEL_PATH = BASE_DIR / "models" / "placement_model.pkl"

# Load dataset and saved model
df = pd.read_csv(DATA_PATH, sep="\t")
model = joblib.load(MODEL_PATH)

features = [
    "ssc_p", "hsc_p", "degree_p", "degree_t",
    "workex", "etest_p", "specialisation", "mba_p"
]

X = df[features]
y = df["status"]

# Recreate the same test split used during training
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Predict test data
predictions = model.predict(X_test)

# Calculate evaluation metrics
print("\n========== MODEL EVALUATION ==========")

print("Accuracy:", round(accuracy_score(y_test, predictions), 4))
print("Precision:", round(precision_score(y_test, predictions, pos_label="Placed"), 4))
print("Recall:", round(recall_score(y_test, predictions, pos_label="Placed"), 4))
print("F1 Score:", round(f1_score(y_test, predictions, pos_label="Placed"), 4))

print("\n========== CONFUSION MATRIX ==========")
print(confusion_matrix(y_test, predictions, labels=["Not Placed", "Placed"]))

print("\n========== CLASSIFICATION REPORT ==========")
print(classification_report(y_test, predictions))