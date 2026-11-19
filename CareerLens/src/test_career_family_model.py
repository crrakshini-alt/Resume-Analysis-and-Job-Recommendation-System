
import joblib

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "career_family_model.pkl"

bundle = joblib.load(MODEL_PATH)
model = bundle["model"]

test_resumes = {
    "IT": """
    Bachelor of Computer Science.
    Python, Java, SQL, HTML, CSS.
    Developed web applications using Flask.
    Knowledge of data structures and algorithms.
    """,

    "Engineering": """
    Mechanical engineering graduate.
    Knowledge of AutoCAD, SolidWorks,
    manufacturing processes and quality control.
    """,

    "Healthcare": """
    Nursing graduate with clinical training,
    patient care, medical records and
    healthcare administration experience.
    """,

    "Finance": """
    Finance graduate with knowledge of
    financial analysis, budgeting,
    investment research and Excel.
    """,

    "Teaching": """
    Education graduate with classroom teaching,
    lesson planning, student assessment
    and communication skills.
    """,

    "Agriculture": """
    Agriculture graduate with knowledge of
    crop production, soil management,
    irrigation and agricultural practices.
    """
}

print("\nCAREER FAMILY MODEL TEST")
print("=" * 55)

for name, resume in test_resumes.items():

    prediction = model.predict([resume])[0]

    print(f"\nTest resume: {name}")
    print(f"Predicted career family: {prediction}")

print("\nTesting completed.")
