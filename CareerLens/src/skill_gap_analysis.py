
# Skills required for different job roles

JOB_ROLES = {
    "Data Scientist": [
        "Python", "SQL", "Pandas", "NumPy",
        "Machine Learning", "Statistics", "Data Visualization"
    ],

    "Data Analyst": [
        "Python", "SQL", "Pandas", "NumPy",
        "Excel", "Power BI", "Data Visualization"
    ],

    "Machine Learning Engineer": [
        "Python", "Machine Learning", "Deep Learning",
        "NumPy", "Pandas", "Scikit-learn",
        "TensorFlow", "Git"
    ],

    "Python Developer": [
        "Python", "SQL", "Flask", "FastAPI",
        "Git", "GitHub"
    ],

    "Web Developer": [
        "HTML", "CSS", "JavaScript",
        "Python", "Flask", "Git", "GitHub"
    ],

    "Game Developer": [
        "C#", "C++", "Unity", "Unreal Engine",
        "Game Development", "2D Game Development",
        "3D Game Development", "Game Physics",
        "Blender", "Git"
    ],
}


# Learning resources for individual skills

LEARNING_RESOURCES = {
    "Python": {
        "title": "Official Python Tutorial",
        "url": "https://docs.python.org/3/tutorial/"
    },
    "SQL": {
        "title": "SQLBolt",
        "url": "https://sqlbolt.com/"
    },
    "Pandas": {
        "title": "Pandas Getting Started",
        "url": "https://pandas.pydata.org/docs/getting_started/"
    },
    "NumPy": {
        "title": "NumPy Quickstart",
        "url": "https://numpy.org/doc/stable/user/quickstart.html"
    },
    "Machine Learning": {
        "title": "Google Machine Learning Crash Course",
        "url": "https://developers.google.com/machine-learning/crash-course"
    },
    "Statistics": {
        "title": "Khan Academy Statistics",
        "url": "https://www.khanacademy.org/math/statistics-probability"
    },
    "Data Visualization": {
        "title": "Matplotlib Tutorials",
        "url": "https://matplotlib.org/stable/tutorials/"
    },
    "Excel": {
        "title": "Microsoft Excel Help and Learning",
        "url": "https://support.microsoft.com/en-us/excel"
    },
    "Power BI": {
        "title": "Microsoft Learn Power BI",
        "url": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi"
    },
    "Deep Learning": {
        "title": "Deep Learning with TensorFlow",
        "url": "https://www.tensorflow.org/tutorials"
    },
    "Scikit-learn": {
        "title": "Scikit-learn Tutorials",
        "url": "https://scikit-learn.org/stable/tutorial/index.html"
    },
    "TensorFlow": {
        "title": "TensorFlow Tutorials",
        "url": "https://www.tensorflow.org/tutorials"
    },
    "Git": {
        "title": "Git Documentation",
        "url": "https://git-scm.com/doc"
    },
    "GitHub": {
        "title": "GitHub Skills",
        "url": "https://skills.github.com/"
    },
    "Flask": {
        "title": "Flask Official Tutorial",
        "url": "https://flask.palletsprojects.com/en/stable/tutorial/"
    },
    "FastAPI": {
        "title": "FastAPI Documentation",
        "url": "https://fastapi.tiangolo.com/tutorial/"
    },
    "HTML": {
        "title": "MDN HTML Tutorial",
        "url": "https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content"
    },
    "CSS": {
        "title": "MDN CSS Tutorial",
        "url": "https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics"
    },
    "JavaScript": {
        "title": "MDN JavaScript Guide",
        "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"
    },
    "C#": {
        "title": "Microsoft Learn C#",
        "url": "https://learn.microsoft.com/en-us/dotnet/csharp/"
    },
    "C++": {
        "title": "Learn C++",
        "url": "https://www.learncpp.com/"
    },
    "Unity": {
        "title": "Unity Learn",
        "url": "https://learn.unity.com/"
    },
    "Unreal Engine": {
        "title": "Unreal Engine Learning",
        "url": "https://dev.epicgames.com/community/learning"
    },
    "Game Development": {
        "title": "Unity Learn",
        "url": "https://learn.unity.com/"
    },
    "2D Game Development": {
        "title": "Unity 2D Learning Resources",
        "url": "https://learn.unity.com/"
    },
    "3D Game Development": {
        "title": "Unity 3D Learning Resources",
        "url": "https://learn.unity.com/"
    },
    "Game Physics": {
        "title": "Unity Physics Documentation",
        "url": "https://docs.unity3d.com/Manual/PhysicsSection.html"
    },
    "Blender": {
        "title": "Blender Tutorials",
        "url": "https://www.blender.org/support/tutorials/"
    },
}


def analyze_skill_gap(candidate_skills, job_role):

    if job_role not in JOB_ROLES:
        raise ValueError(f"Unknown job role: {job_role}")

    required_skills = JOB_ROLES[job_role]

    # Case-insensitive skill matching
    candidate_skill_set = {
        skill.strip().lower()
        for skill in candidate_skills
    }

    matched_skills = []
    missing_skills = []

    for skill in required_skills:
        if skill.lower() in candidate_skill_set:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    match_percentage = (
        len(matched_skills) / len(required_skills)
    ) * 100 if required_skills else 0

    # Find learning resources for missing skills
    learning_resources = []

    for skill in missing_skills:
        resource = LEARNING_RESOURCES.get(skill)

        if resource:
            learning_resources.append({
                "skill": skill,
                "title": resource["title"],
                "url": resource["url"]
            })

    return {
        "job_role": job_role,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percentage": round(match_percentage, 2),
        "learning_resources": learning_resources
    }
