
# Interview questions based on technical skills

INTERVIEW_QUESTIONS = {

    "Python": [
        "What are the differences between a list and a tuple?",
        "What is the difference between == and is?",
        "What are Python dictionaries?",
        "What is the purpose of functions in Python?"
    ],

    "Java": [
        "What is the difference between JDK, JRE and JVM?",
        "What is inheritance in Java?",
        "What is polymorphism?"
    ],

    "SQL": [
        "What is the difference between DELETE and DROP?",
        "What is a primary key?",
        "What is the difference between WHERE and HAVING?"
    ],

    "Machine Learning": [
        "What is supervised learning?",
        "What is the difference between classification and regression?",
        "What is overfitting in Machine Learning?"
    ],

    "Deep Learning": [
        "What is an artificial neural network?",
        "What is an activation function?",
        "What is the difference between ANN and CNN?"
    ],

    "Pandas": [
        "What is Pandas in Python?",
        "What is a DataFrame?",
        "How do you handle missing values using Pandas?"
    ],

    "NumPy": [
        "What is NumPy?",
        "What is an ndarray?",
        "What is the difference between a list and a NumPy array?"
    ],

    "Data Visualization": [
        "What is data visualization?",
        "What is the difference between a bar chart and a histogram?",
        "Why are graphs useful in data analysis?"
    ],

    "HTML": [
        "What is HTML?",
        "What are HTML tags?",
        "What is the difference between div and span?"
    ],

    "CSS": [
        "What is CSS?",
        "What is the CSS box model?",
        "What is the difference between class and ID selectors?"
    ],

    "JavaScript": [
        "What is JavaScript?",
        "What is the difference between let, const and var?",
        "What is the DOM?"
    ],

    "Flask": [
        "What is Flask?",
        "What is routing in Flask?",
        "What are templates in Flask?"
    ],

    "FastAPI": [
        "What is FastAPI?",
        "What is an API endpoint?",
        "What is the difference between GET and POST?"
    ],

    "Git": [
        "What is Git?",
        "What is the difference between Git and GitHub?",
        "What is a Git commit?"
    ],

    "GitHub": [
        "What is GitHub?",
        "What is a repository?",
        "What is a pull request?"
    ],

    "Scikit-learn": [
        "What is Scikit-learn?",
        "What is train-test splitting?",
        "What is a confusion matrix?"
    ],

    "TensorFlow": [
        "What is TensorFlow?",
        "What is a tensor?",
        "What is a neural network?"
    ],

    "Statistics": [
        "What is the difference between mean, median and mode?",
        "What is standard deviation?",
        "What is correlation?"
    ],

    "Excel": [
        "What is a pivot table?",
        "What is VLOOKUP?",
        "What is conditional formatting?"
    ],

    "Power BI": [
        "What is Power BI?",
        "What is a dashboard?",
        "What is the difference between Power BI and Excel?"
    ],

    "Data Analysis": [
        "What is data analysis?",
        "What are the steps involved in data analysis?",
        "What is data cleaning?"
    ]
}


def generate_interview_questions(candidate_skills):

    questions = []

    for skill in candidate_skills:

        if skill in INTERVIEW_QUESTIONS:

            skill_questions = INTERVIEW_QUESTIONS[skill]

            for question in skill_questions:
                questions.append({
                    "skill": skill,
                    "question": question
                })

    return questions
