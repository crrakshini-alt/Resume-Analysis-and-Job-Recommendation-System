import joblib
import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "placement_model.pkl"

# Load trained model
model = joblib.load(MODEL_PATH)

# Get Logistic Regression classifier
classifier = model.named_steps["classifier"]

# Get feature names after preprocessing
preprocessor = model.named_steps["preprocessor"]
feature_names = preprocessor.get_feature_names_out()

# Get model coefficients
coefficients = classifier.coef_[0]

# Create feature importance table
importance = pd.DataFrame({
    "Feature": feature_names,
    "Coefficient": coefficients
})

importance["Absolute Value"] = importance["Coefficient"].abs()

importance = importance.sort_values(
    by="Absolute Value",
    ascending=False
)

print("\n========== MODEL FEATURE ANALYSIS ==========")
print(importance.to_string(index=False))