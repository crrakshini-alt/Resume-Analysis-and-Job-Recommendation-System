
import re

# Expandable developer-role catalogue.
# Specific evidence is more important than generic programming skills.

ROLE_PROFILES = {
    "Frontend Developer": {
        "keywords": [
            "html", "css", "javascript", "typescript", "react",
            "angular", "vue", "frontend", "front end",
            "responsive design", "dom manipulation"
        ],"required": [
    "javascript",
    "react",
    "angular",
    "vue",
    "typescript"
],"required": ["html", "css"],
        "strong": ["react", "angular", "vue", "javascript", "typescript"]
    },

    "Backend Developer": {
        "keywords": [
            "python", "java", "node.js", "nodejs", "django",
            "flask", "fastapi", "spring boot", "express.js",
            "backend", "back end", "rest api", "database integration"
        ],
        "required": ["backend", "back end", "django", "flask",
                     "fastapi", "spring boot", "express.js"],
        "strong": ["django", "flask", "fastapi", "spring boot",
                   "express.js", "rest api"]
    },

    "Full Stack Developer": {
        "keywords": [
            "html", "css", "javascript", "react", "node.js",
            "python", "sql", "frontend", "backend",
            "full stack", "django", "flask", "fastapi"
        ],
        "required": ["full stack"],
        "strong": ["react", "node.js", "django", "flask",
                   "fastapi", "frontend", "backend"]
    },

    "Web Developer": {
        "keywords": [
            "html", "css", "javascript", "web development",
            "responsive design", "react", "php", "website"
        ],
        "required": [
    "javascript",
    "react",
    "angular",
    "vue",
    "typescript",
    "web development"
],
        "strong": ["javascript", "react", "responsive design"]
    },

    "Python Developer": {
        "keywords": [
            "python", "django", "flask", "fastapi", "pandas",
            "numpy", "automation", "python development",
            "pytest", "python scripting"
        ],
        "required": ["python"],
        "strong": ["django", "flask", "fastapi",
                   "python development", "python scripting",
                   "pytest", "automation"]
    },

    "Java Developer": {
        "keywords": [
            "java", "spring boot", "hibernate", "maven",
            "gradle", "junit", "java development"
        ],
        "required": ["java"],
        "strong": ["spring boot", "hibernate", "maven",
                   "gradle", "junit"]
    },

    "C++ Developer": {
        "keywords": [
            "c++", "cpp", "stl", "c++ development",
            "object oriented programming", "data structures",
            "algorithms"
        ],
        "required": ["c++", "cpp"],
        "strong": ["stl", "c++ development"]
    },

    "C# Developer": {
        "keywords": [
            "c#", "c sharp", ".net", "asp.net",
            "entity framework", "visual studio"
        ],
        "required": ["c#", "c sharp"],
        "strong": [".net", "asp.net", "entity framework"]
    },

    "JavaScript Developer": {
        "keywords": [
            "javascript", "typescript", "node.js", "nodejs",
            "react", "angular", "vue"
        ],
        "required": ["javascript", "typescript"],
        "strong": ["node.js", "nodejs", "react", "angular", "vue"]
    },

    "PHP Developer": {
        "keywords": [
            "php", "laravel", "symfony", "wordpress",
            "mysql", "php development"
        ],
        "required": ["php"],
        "strong": ["laravel", "symfony", "wordpress"]
    },

    "Go Developer": {
        "keywords": [
            "golang", "go language", "go programming",
            "grpc", "microservices"
        ],
        "required": ["golang", "go programming", "go language"],
        "strong": ["grpc", "microservices"]
    },

    "Mobile App Developer": {
        "keywords": [
            "android", "ios", "flutter", "react native",
            "mobile app", "mobile development"
        ],
        "required": ["mobile app", "mobile development"],
        "strong": ["flutter", "react native", "android", "ios"]
    },

    "Android Developer": {
        "keywords": [
            "android", "kotlin", "java", "android studio",
            "jetpack compose"
        ],
        "required": ["android"],
        "strong": ["kotlin", "android studio", "jetpack compose"]
    },

    "iOS Developer": {
        "keywords": [
            "ios", "swift", "swiftui", "xcode",
            "objective-c", "iphone app"
        ],
        "required": ["ios"],
        "strong": ["swift", "swiftui", "xcode", "objective-c"]
    },

    "Flutter Developer": {
        "keywords": [
            "flutter", "dart", "mobile app", "firebase",
            "cross platform"
        ],
        "required": ["flutter"],
        "strong": ["dart", "firebase", "cross platform"]
    },

    "React Native Developer": {
        "keywords": [
            "react native", "javascript", "typescript",
            "mobile app", "expo"
        ],
        "required": ["react native"],
        "strong": ["expo", "typescript", "mobile app"]
    },

    "Game Developer": {
        "keywords": [
            "game development", "unity", "unreal engine",
            "godot", "gameplay programming", "game physics",
            "collision detection", "blender",
            "3d game development", "2d game development"
        ],
        "required": ["game development", "gameplay programming",
                     "2d game development", "3d game development"],
        "strong": ["unity", "unreal engine", "godot",
                   "game physics", "gameplay programming"]
    },

    "Unity Developer": {
        "keywords": [
            "unity", "c#", "game development",
            "gameplay programming", "3d game development"
        ],
        "required": ["unity"],
        "strong": ["c#", "gameplay programming", "game development"]
    },

    "Unreal Engine Developer": {
        "keywords": [
            "unreal engine", "c++", "blueprints",
            "game development", "gameplay programming"
        ],
        "required": ["unreal engine"],
        "strong": ["blueprints", "gameplay programming", "c++"]
    },

    "AI Developer": {
        "keywords": [
            "artificial intelligence", "machine learning",
            "deep learning", "python", "tensorflow",
            "pytorch", "scikit-learn"
        ],
        "required": ["artificial intelligence", "machine learning"],
        "strong": ["deep learning", "tensorflow", "pytorch",
                   "scikit-learn"]
    },

    "Machine Learning Engineer": {
        "keywords": [
            "machine learning", "deep learning", "python",
            "tensorflow", "pytorch", "scikit-learn",
            "model training", "model deployment"
        ],
        "required": ["machine learning"],
        "strong": ["deep learning", "model training",
                   "model deployment", "tensorflow", "pytorch"]
    },

    "Data Engineer": {
        "keywords": [
            "data engineering", "sql", "python",
            "apache spark", "airflow", "etl",
            "data pipelines", "data warehouse"
        ],
        "required": ["data engineering", "apache spark",
                     "airflow", "etl", "data pipelines",
                     "data warehouse"],
        "strong": ["apache spark", "airflow", "etl",
                   "data pipelines", "data warehouse"]
    },

    "Cloud Developer": {
        "keywords": [
            "aws", "azure", "google cloud", "docker",
            "kubernetes", "cloud computing", "cloud development"
        ],
        "required": ["cloud computing", "cloud development",
                     "aws", "azure", "google cloud"],
        "strong": ["docker", "kubernetes", "aws", "azure"]
    },

    "DevOps Engineer": {
        "keywords": [
            "docker", "kubernetes", "jenkins", "ci/cd",
            "linux", "terraform", "github actions"
        ],
        "required": ["ci/cd", "terraform", "jenkins",
                     "kubernetes", "github actions"],
        "strong": ["docker", "kubernetes", "terraform",
                   "jenkins", "github actions"]
    },

    "Embedded Systems Developer": {
        "keywords": [
            "embedded systems", "embedded c", "c++",
            "microcontrollers", "arduino", "raspberry pi",
            "firmware", "rtos"
        ],
        "required": ["embedded systems", "embedded c",
                     "microcontrollers", "arduino", "raspberry pi"],
        "strong": ["rtos", "firmware", "microcontrollers"]
    },

    "Firmware Developer": {
        "keywords": [
            "firmware", "embedded c", "microcontrollers",
            "rtos", "hardware"
        ],
        "required": ["firmware", "embedded c"],
        "strong": ["microcontrollers", "rtos"]
    },

    "Cybersecurity Software Developer": {
        "keywords": [
            "cybersecurity", "secure coding",
            "application security", "penetration testing",
            "network security", "security software"
        ],
        "required": ["secure coding", "application security",
                     "security software"],
        "strong": ["penetration testing", "network security"]
    },

    "Blockchain Developer": {
        "keywords": [
            "blockchain", "solidity", "ethereum",
            "smart contracts", "web3", "hardhat"
        ],
        "required": ["blockchain", "solidity", "smart contracts"],
        "strong": ["ethereum", "web3", "hardhat"]
    },

    "Database Developer": {
        "keywords": [
            "sql", "mysql", "postgresql", "oracle",
            "database design", "stored procedures"
        ],
        "required": ["database design", "stored procedures"],
        "strong": ["mysql", "postgresql", "oracle"]
    },

    "Software Developer": {
        "keywords": [
            "software development", "software engineering",
            "data structures", "algorithms", "python",
            "java", "c++", "object oriented programming"
        ],
        "required": ["software development", "software engineering"],
        "strong": ["data structures", "algorithms",
                   "object oriented programming"]
    },

    "API Developer": {
        "keywords": [
            "api development", "rest api", "fastapi",
            "django rest framework", "express.js",
            "graphql", "microservices"
        ],
        "required": ["api development", "rest api",
                     "django rest framework", "graphql"],
        "strong": ["fastapi", "express.js", "microservices"]
    },

    "AR/VR Developer": {
        "keywords": [
            "augmented reality", "virtual reality",
            "ar development", "vr development",
            "arcore", "arkit", "openxr", "oculus",
            "mixed reality", "3d development"
        ],
        "required": ["augmented reality", "virtual reality",
                     "ar development", "vr development",
                     "arcore", "arkit", "openxr",
                     "mixed reality"],
        "strong": ["arcore", "arkit", "openxr", "oculus"]
    },

    "Robotics Software Developer": {
        "keywords": [
            "robotics", "ros", "robot operating system",
            "ros2", "robotics software", "motion planning",
            "robot control", "computer vision"
        ],
        "required": ["robotics", "ros", "robot operating system",
                     "ros2", "robotics software"],
        "strong": ["motion planning", "robot control", "ros2"]
    },

    "Computer Vision Developer": {
        "keywords": [
            "computer vision", "opencv", "image processing",
            "python", "deep learning", "pytorch"
        ],
        "required": ["computer vision", "opencv", "image processing"],
        "strong": ["opencv", "image processing", "pytorch"]
    },

    "NLP Developer": {
        "keywords": [
            "natural language processing", "nlp",
            "transformers", "large language models",
            "python", "pytorch", "tensorflow"
        ],
        "required": ["natural language processing", "nlp",
                     "transformers", "large language models"],
        "strong": ["transformers", "large language models",
                   "pytorch", "tensorflow"]
    },
}


def _contains_evidence(text, phrase):
    """Find a phrase without matching inside unrelated words."""
    phrase = phrase.lower().strip()

    if not phrase:
        return False

    pattern = r"(?<!\w)" + re.escape(phrase) + r"(?!\w)"
    return re.search(pattern, text, re.IGNORECASE) is not None


def get_developer_role_matches(resume_text, limit=15):
    """
    Match developer roles using resume evidence.

    Scores are evidence-match scores, NOT ML probabilities,
    candidate proficiency scores, or hiring predictions.
    """

    if not resume_text or not resume_text.strip():
        return []

    text = resume_text.lower()
    results = []

    for role, profile in ROLE_PROFILES.items():

        keywords = profile["keywords"]
        required = profile["required"]
        strong = profile["strong"]

        matched = [
            keyword for keyword in keywords
            if _contains_evidence(text, keyword)
        ]

        matched_required = [
            keyword for keyword in required
            if _contains_evidence(text, keyword)
        ]

        matched_strong = [
            keyword for keyword in strong
            if _contains_evidence(text, keyword)
        ]

        # A role must have at least one distinctive signal.
        if not matched_required:
            continue

        if len(matched) < 2:
            continue

        # Calculate evidence score.
        # Strong and required terms receive higher importance.
        total_weight = 0
        earned_weight = 0

        for keyword in keywords:
            weight = 1

            if keyword in required:
                weight = 3
            elif keyword in strong:
                weight = 2

            total_weight += weight

            if keyword in matched:
                earned_weight += weight

        score = (earned_weight / total_weight) * 100

        results.append({
            "job_role": role,
            "match_score": round(score, 2),
            "matched_evidence": matched,
            "evidence_count": len(matched),
            "strong_evidence": matched_strong,
            "score_type": "Weighted resume skill/evidence match"
        })

    results.sort(
        key=lambda item: (
            item["match_score"],
            item["evidence_count"]
        ),
        reverse=True
    )

    return results[:limit]


def predict_developer_roles(resume_text):
    """Return evidence-supported developer-role matches."""
    return get_developer_role_matches(resume_text)
