import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "dataset"

files = ["train.xlsx", "data_description_doc.xlsx"]

for file in files:
    file_path = DATASET_DIR / file

    print(f"\n========== {file} ==========")

    if not file_path.exists():
        print("File not found:", file_path)
        continue

    if file == "train.xlsx":
        df = pd.read_csv(file_path, sep="\t")
        print("Format: TSV")
        print("Rows:", df.shape[0])
        print("Columns:", df.shape[1])
        print("\nColumn names:")
        print(df.columns.tolist())
        print("\nFirst 5 records:")
        print(df.head())
        print("\nMissing values:")
        print(df.isnull().sum())

    else:
        try:
            excel = pd.ExcelFile(file_path)
            print("Sheets:", excel.sheet_names)

            for sheet in excel.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet)
                print(f"\n--- Sheet: {sheet} ---")
                print(df.head())

        except Exception as e:
            print("Could not read this file:", e)