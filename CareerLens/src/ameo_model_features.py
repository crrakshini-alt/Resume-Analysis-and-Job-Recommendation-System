import pandas as pd

df = pd.read_csv("dataset/ameo_cleaned.csv")

target = "Salary"

features = [
    "10percentage",
    "12percentage",
    "12graduation",
    "CollegeTier",
    "collegeGPA",
    "CollegeCityTier",
    "GraduationYear",
    "English",
    "Logical",
    "Quant",
    "conscientiousness",
    "agreeableness",
    "extraversion",
    "nueroticism",
    "openess_to_experience",
    "Gender",
    "Degree",
    "Specialization",
    "CollegeState"
]

X = df[features]
y = df[target]

print("Input records:", X.shape[0])
print("Input features:", X.shape[1])
print("Target:", target)
print("Missing values:", X.isnull().sum().sum())
print("Target missing values:", y.isnull().sum())
