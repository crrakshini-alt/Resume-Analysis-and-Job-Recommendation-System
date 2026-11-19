
from pathlib import Path
from resume_parser import extract_resume_text
from predict_roles import predict_roles

BASE_DIR = Path(__file__).resolve().parent.parent
PDF_PATH = BASE_DIR / "resumes" / "sample_resume.pdf"

if not PDF_PATH.exists():
    print("Resume PDF not found!")
else:
    # Extract text from PDF
    resume_text = extract_resume_text(PDF_PATH)

    print("\nEXTRACTED RESUME TEXT:")
    print(resume_text[:1000])

    # Predict job roles
    results = predict_roles(resume_text)

    print("\nPREDICTED JOB ROLES:")
    if results:
        for result in results:
            print(
                result["job_role"],
                "-",
                result["score"],
                "%"
            )
    else:
        print("No predictions generated.")
