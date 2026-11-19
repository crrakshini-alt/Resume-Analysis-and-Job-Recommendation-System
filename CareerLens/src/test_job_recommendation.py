
from pathlib import Path

from resume_parser import extract_resume_text
from skill_extractor import extract_skills
from job_recommendation import recommend_job_roles

BASE_DIR = Path(__file__).resolve().parent.parent

resume_path = BASE_DIR / "resumes" / "sample_resume.pdf"

# Extract resume text
resume_text = extract_resume_text(resume_path)

# Extract skills
candidate_skills = extract_skills(resume_text)

# Recommend job roles
recommendations = recommend_job_roles(candidate_skills)

print("\n========== JOB ROLE RECOMMENDATIONS ==========")

for number, result in enumerate(recommendations, start=1):

    print(f"\n{number}. {result['job_role']}")

    print("Skill Match:", result["match_percentage"], "%")

    print("Missing Skills:", result["missing_skills"])
