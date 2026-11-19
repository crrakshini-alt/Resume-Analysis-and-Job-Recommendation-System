import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR / "dataset" / "placement_data_full_class.csv"
)

# Load dataset
df = pd.read_csv(DATA_PATH, sep="\t")

# Select input features
features = [
    "ssc_p",
    "hsc_p",
    "degree_p",
    "degree_t",
    "workex",
    "etest_p",
    "specialisation",
    "mba_p"
]

X = df[features]

# Select target
y = df["status"]

# Separate numerical and categorical columns
numerical_features = [
    "ssc_p",
    "hsc_p",
    "degree_p",
    "etest_p",
    "mba_p"
]

categorical_features = [
    "degree_t",
    "workex",
    "specialisation"
]

# Prepare numerical features
numerical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median"))
    ]
)

# Prepare categorical features
categorical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ]
)

# Combine transformations
preprocessor = ColumnTransformer(
    transformers=[
        ("num", numerical_transformer, numerical_features),
        ("cat", categorical_transformer, categorical_features)
    ]
)

# Divide into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Fit transformations using training data only
X_train_prepared = preprocessor.fit_transform(X_train)

# Transform testing data
X_test_prepared = preprocessor.transform(X_test)

print("\n========== DATASET PREPARATION ==========")

print("Original records:", len(df))
print("Selected features:", len(features))

print("Training records:", X_train.shape[0])
print("Testing records:", X_test.shape[0])

print("Training feature shape:", X_train_prepared.shape)
print("Testing feature shape:", X_test_prepared.shape)

print("\nTraining target distribution:")
print(y_train.value_counts())

print("\nTesting target distribution:")
print(y_test.value_counts())

print("\nDataset preparation completed!")