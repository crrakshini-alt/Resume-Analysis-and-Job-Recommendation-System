import joblib
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "career_family_model.pkl"

# Load trained career-family model
bundle = joblib.load(MODEL_PATH)
model = bundle["model"]


def predict_career_family(resume_text):
    """
    Predict the broad career family from resume text.
    """

    if not resume_text or not resume_text.strip():
        return None

    prediction = model.predict([resume_text])[0]

    return str(prediction)


if __name__ == "__main__":

    sample_resume = """
    Bachelor of Computer Science.
    Python, SQL, Machine Learning, Data Analysis,
    Flask, Pandas and Scikit-learn.
    """

    result = predict_career_family(sample_resume)

    print("Predicted Career Family:", result)