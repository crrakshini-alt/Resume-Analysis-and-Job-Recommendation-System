import pandas as pd

df = pd.read_csv("dataset/ameo_cleaned.csv")

target = "Salary"

excluded = [
    "Salary", "DOJ", "DOL", "Designation",
    "JobCity", "DOB", "CollegeID",
    "CollegeCityID", "10board", "12board"
]

features = df.drop(columns=excluded)

print("TARGET:", target)
print("\nFEATURE COUNT:", len(features.columns))
print("\nNUMERIC FEATURES:")
print(features.select_dtypes(include="number").columns.tolist())

print("\nCATEGORICAL FEATURES:")
print(features.select_dtypes(exclude="number").columns.tolist())

print("\nMISSING VALUES:")
print(features.isnull().sum()[features.isnull().sum() > 0])