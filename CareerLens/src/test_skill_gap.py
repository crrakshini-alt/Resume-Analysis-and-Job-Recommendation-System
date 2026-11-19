
from resume_parser import extract_resume_text
from skill_extractor import extract_skills
from skill_gap_analysis import analyze_skill_gap, JOB_ROLES

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

resume_path = BASE_DIR / "resumes" / "sample_resume.pdf"

# Extract resume text
resume_text = extract_resume_text(resume_path)

# Extract candidate skills
candidate_skills = extract_skills(resume_text)

# Display available job roles
print("\nAvailable Job Roles:")

for number, role in enumerate(JOB_ROLES, start=1):
    print(number, role)

# Select a job role
choice = int(input("\nSelect a job role (1-5): "))

job_role = list(JOB_ROLES.keys())[choice - 1]

# Analyze skill gap
result = analyze_skill_gap(candidate_skills, job_role)

# Display results
print("\n========== SKILL GAP REPORT ==========")

print("Job Role:", result["job_role"])

print("\nMatched Skills:")
for skill in result["matched_skills"]:
    print("-", skill)

print("\nMissing Skills:")
for skill in result["missing_skills"]:
    print("-", skill)

print("\nSkill Match Percentage:",
      result["match_percentage"], "%")
