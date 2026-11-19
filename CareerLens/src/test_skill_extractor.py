from resume_parser import extract_resume_text
from skill_extractor import extract_skills
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

resume_path = BASE_DIR / "resumes" / "sample_resume.pdf"

resume_text = extract_resume_text(resume_path)

skills = extract_skills(resume_text)

print("\n========== EXTRACTED SKILLS ==========")

for skill in skills:
    print("-", skill)