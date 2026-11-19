
from pathlib import Path

from resume_parser import extract_resume_text
from skill_extractor import extract_skills
from interview_question_generator import generate_interview_questions

BASE_DIR = Path(__file__).resolve().parent.parent

resume_path = BASE_DIR / "resumes" / "sample_resume.pdf"

# Extract resume text
resume_text = extract_resume_text(resume_path)

# Extract skills
candidate_skills = extract_skills(resume_text)

# Generate interview questions
questions = generate_interview_questions(candidate_skills)

print("\n========== INTERVIEW QUESTIONS ==========")

for item in questions:

    print("\nSkill:", item["skill"])
    print("Question:", item["question"])
