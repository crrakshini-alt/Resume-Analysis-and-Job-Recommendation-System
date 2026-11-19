
from pathlib import Path
import pandas as pd
from huggingface_hub import hf_hub_download

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "career_datasets" / "external_raw"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("Downloading external resume dataset...")

file_path = hf_hub_download(
    repo_id="mithinsagar/exai-resumeintel-data",
    filename="clean_resume_data.csv",
    repo_type="dataset",
    local_dir=str(OUTPUT_DIR)
)

df = pd.read_csv(file_path)

print("\nDOWNLOAD COMPLETED")
print("=" * 55)

print("File:", file_path)
print("Total resumes:", len(df))
print("Columns:", df.columns.tolist())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate IDs:", df["ID"].duplicated().sum())
print("Duplicate resume texts:", df["Feature"].duplicated().sum())

print("\nCategory distribution:")
print(df["Category"].value_counts().to_string())

print("\nSaved original dataset separately.")
print("No existing project dataset was modified.")
