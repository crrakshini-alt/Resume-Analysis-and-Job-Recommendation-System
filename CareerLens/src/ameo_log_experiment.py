import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# Load cleaned dataset
data = pd.read_csv("dataset/ameo_cleaned.csv")

# Select input features
numeric_features = [
    "10percentage", "12percentage", "12graduation",
    "CollegeTier", "CollegeCityTier", "GraduationYear",
    "English", "Logical", "Quant",
    "conscientiousness", "agreeableness",
    "extraversion", "nueroticism", "openess_to_experience"
]

categorical_features = [
    "Gender", "Degree", "Specialization", "CollegeState"
]

features = numeric_features + categorical_features

X = data[features]
y = data["Salary"]

# Same train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Preprocessing
numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("num", numeric_transformer, numeric_features),
    ("cat", categorical_transformer, categorical_features)
])

# Train using log-transformed salary
model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", LinearRegression())
])

model.fit(X_train, np.log1p(y_train))

# Convert predictions back to rupees
log_predictions = model.predict(X_test)
predictions = np.expm1(log_predictions)

# Evaluation
mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
r2 = r2_score(y_test, predictions)

print("\nLINEAR REGRESSION WITH LOG-TRANSFORMED SALARY")
print("---------------------------------------------")
print(f"MAE: ₹{mae:.2f}")
print(f"RMSE: ₹{rmse:.2f}")
print(f"R2 Score: {r2:.4f}")