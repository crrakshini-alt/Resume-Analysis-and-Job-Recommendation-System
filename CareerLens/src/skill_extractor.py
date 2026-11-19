
import re

SKILLS = [
    # Programming languages
    "Python",
    "Java",
    "C#",
    "C++",
    "C",
    "JavaScript",

    # Game development
    "Unity",
    "Unreal Engine",
    "Godot",
    "Blender",
    "Game Development",
    "2D Game Development",
    "3D Game Development",
    "Game Physics",
    "Gameplay Programming",
    "Collision Detection",
    "Scene Management",

    # Data science and machine learning
    "Machine Learning",
    "Deep Learning",
    "SQL",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "TensorFlow",
    "Data Analysis",
    "Data Visualization",
    "Statistics",
    "Power BI",

    # Web development
    "HTML",
    "CSS",
    "Flask",
    "FastAPI",

    # Tools
    "Visual Studio",
    "Git",
    "GitHub"
]


def extract_skills(resume_text):
    found_skills = []

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, resume_text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills


if __name__ == "__main__":
    sample = """
    Skills: C#, C++, Unity, Unreal Engine,
    Blender, Python and Game Physics.
    """

    print(extract_skills(sample))
