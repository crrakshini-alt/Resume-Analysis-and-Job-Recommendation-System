import joblib
import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "placement_model.pkl"
OUTPUT_PATH = BASE_DIR / "dataset" / "batch_predictions.csv"

# Load trained model
model = joblib.load(MODEL_PATH)

# Sample test candidates
candidates = pd.DataFrame([
    {
        "ssc_p": 80, "hsc_p": 75, "degree_p": 78,
        "degree_t": "Sci&Tech", "workex": "No",
        "etest_p": 85, "specialisation": "Mkt&HR", "mba_p": 70
    },
    {
        "ssc_p": 65, "hsc_p": 60, "degree_p": 62,
        "degree_t": "Comm&Mgmt", "workex": "Yes",
        "etest_p": 70, "specialisation": "Mkt&Fin", "mba_p": 65
    },
    {
        "ssc_p": 90, "hsc_p": 85, "degree_p": 88,
        "degree_t": "Sci&Tech", "workex": "Yes",
        "etest_p": 90, "specialisation": "Mkt&Fin", "mba_p": 85
    }
])

# Predict placement status
predictions = model.predict(candidates)
probabilities = model.predict_proba(candidates)

# Add predictions to candidate records
results = candidates.copy()
results["Predicted_Status"] = predictions

for index, status in enumerate(model.classes_):
    results[f"{status}_Probability"] = probabilities[:, index] * 100

# Save results
results.to_csv(OUTPUT_PATH, index=False)

print("\n========== BATCH PREDICTION RESULTS ==========")
print(results.to_string(index=False))

print("\nResults saved to:", OUTPUT_PATH)
