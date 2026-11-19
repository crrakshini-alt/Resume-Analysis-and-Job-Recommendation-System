import joblib
import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "placement_model.pkl"

# Load trained model
model = joblib.load(MODEL_PATH)

# New candidate details
candidate = pd.DataFrame([{
    "ssc_p": 80,
    "hsc_p": 75,
    "degree_p": 78,
    "degree_t": "Sci&Tech",
    "workex": "No",
    "etest_p": 85,
    "specialisation": "Mkt&HR",
    "mba_p": 70
}])

# Predict placement status
prediction = model.predict(candidate)

# Prediction probabilities
probabilities = model.predict_proba(candidate)[0]

print("\n========== CANDIDATE PREDICTION ==========")
print("Predicted Status:", prediction[0])

for status, probability in zip(model.classes_, probabilities):
    print(f"{status}: {probability * 100:.2f}%")