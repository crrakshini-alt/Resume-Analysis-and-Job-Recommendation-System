import joblib
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "resume_role_model.pkl"

# Load trained role prediction model
bundle = joblib.load(MODEL_PATH)

model = bundle["model"]
vectorizer = bundle["vectorizer"]
label_encoder = bundle["label_encoder"]
threshold = bundle["threshold"]


def get_all_role_scores(resume_text):
    """
    Calculate scores for all supported IT job roles.
    """

    if not resume_text or not resume_text.strip():
        return []

    resume_vector = vectorizer.transform([resume_text])

    scores = model.predict_proba(resume_vector)[0]

    results = []

    for i in range(len(scores)):
        results.append({
            "job_role": label_encoder.classes_[i],
            "score": round(float(scores[i]) * 100, 2)
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results


def predict_roles(resume_text):
    """
    Return only roles that meet the model threshold.
    """

    all_scores = get_all_role_scores(resume_text)

    if not all_scores:
        return []

    predictions = [
        result
        for result in all_scores
        if result["score"] >= threshold * 100
    ]

    return predictions