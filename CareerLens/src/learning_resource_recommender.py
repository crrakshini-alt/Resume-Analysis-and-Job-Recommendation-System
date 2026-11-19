
from urllib.parse import quote_plus


# Curated learning resources for common skills
LEARNING_RESOURCES = {
    "python": [
        {
            "title": "Python Official Tutorial",
            "platform": "Python Documentation",
            "type": "Documentation",
            "url": "https://docs.python.org/3/tutorial/",
            "cost": "Free"
        },
        {
            "title": "Python Course",
            "platform": "Kaggle Learn",
            "type": "Course",
            "url": "https://www.kaggle.com/learn/python",
            "cost": "Free"
        }
    ],

    "sql": [
        {
            "title": "Learn SQL",
            "platform": "SQLBolt",
            "type": "Interactive Tutorial",
            "url": "https://sqlbolt.com/",
            "cost": "Free"
        }
    ],

    "pandas": [
        {
            "title": "Pandas Getting Started",
            "platform": "Pandas Documentation",
            "type": "Documentation",
            "url": "https://pandas.pydata.org/docs/getting_started/",
            "cost": "Free"
        },
        {
            "title": "Pandas Course",
            "platform": "Kaggle Learn",
            "type": "Course",
            "url": "https://www.kaggle.com/learn/pandas",
            "cost": "Free"
        }
    ],

    "numpy": [
        {
            "title": "NumPy Learning Resources",
            "platform": "NumPy",
            "type": "Documentation",
            "url": "https://numpy.org/learn/",
            "cost": "Free"
        }
    ],

    "machine learning": [
        {
            "title": "Machine Learning Crash Course",
            "platform": "Google",
            "type": "Course",
            "url": "https://developers.google.com/machine-learning/crash-course",
            "cost": "Free"
        },
        {
            "title": "Intro to Machine Learning",
            "platform": "Kaggle Learn",
            "type": "Course",
            "url": "https://www.kaggle.com/learn/intro-to-machine-learning",
            "cost": "Free"
        }
    ],

    "statistics": [
        {
            "title": "Statistics and Probability",
            "platform": "Khan Academy",
            "type": "Course",
            "url": "https://www.khanacademy.org/math/statistics-probability",
            "cost": "Free"
        }
    ],

    "data visualization": [
        {
            "title": "Data Visualization Course",
            "platform": "Kaggle Learn",
            "type": "Course",
            "url": "https://www.kaggle.com/learn/data-visualization",
            "cost": "Free"
        }
    ],

    "excel": [
        {
            "title": "Excel Help and Learning",
            "platform": "Microsoft",
            "type": "Tutorial",
            "url": "https://support.microsoft.com/en-us/excel",
            "cost": "Free"
        }
    ],

    "power bi": [
        {
            "title": "Power BI Learning",
            "platform": "Microsoft Learn",
            "type": "Course",
            "url": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi/",
            "cost": "Free"
        }
    ],

    "javascript": [
        {
            "title": "JavaScript Guide",
            "platform": "MDN",
            "type": "Documentation",
            "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide",
            "cost": "Free"
        }
    ],

    "django": [
        {
            "title": "Django Getting Started",
            "platform": "Django Documentation",
            "type": "Documentation",
            "url": "https://docs.djangoproject.com/en/stable/intro/",
            "cost": "Free"
        }
    ],

    "fastapi": [
        {
            "title": "FastAPI Tutorial",
            "platform": "FastAPI Documentation",
            "type": "Documentation",
            "url": "https://fastapi.tiangolo.com/tutorial/",
            "cost": "Free"
        }
    ],

    "scikit-learn": [
        {
            "title": "Scikit-learn User Guide",
            "platform": "Scikit-learn",
            "type": "Documentation",
            "url": "https://scikit-learn.org/stable/user_guide.html",
            "cost": "Free"
        }
    ],

    "tensorflow": [
        {
            "title": "TensorFlow Tutorials",
            "platform": "TensorFlow",
            "type": "Tutorial",
            "url": "https://www.tensorflow.org/tutorials",
            "cost": "Free"
        }
    ]
}


# Handle different names for the same skill
SKILL_ALIASES = {
    "ml": "machine learning",
    "powerbi": "power bi",
    "js": "javascript",
    "sklearn": "scikit-learn"
}


def recommend_resources(missing_skills, max_resources_per_skill=3):

    recommendations = []

    if not missing_skills:
        return recommendations

    for skill in missing_skills:

        normalized_skill = str(skill).strip().lower()

        # Convert aliases into standard skill names
        normalized_skill = SKILL_ALIASES.get(
            normalized_skill,
            normalized_skill
        )

        resources = LEARNING_RESOURCES.get(normalized_skill)

        # Use a YouTube search link if no curated resource exists
        if resources is None:
            resources = [
                {
                    "title": f"{skill} Tutorials for Beginners",
                    "platform": "YouTube",
                    "type": "Video Search",
                    "url": (
                        "https://www.youtube.com/results?search_query="
                        + quote_plus(f"{skill} tutorials for beginners")
                    ),
                    "cost": "Free"
                }
            ]

        recommendations.append({
            "skill": str(skill),
            "resources": resources[:max_resources_per_skill]
        })

    return recommendations
