from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DOC_PATH = BASE_DIR / "dataset" / "data_description_doc.xlsx"

with open(DOC_PATH, "r", encoding="utf-8") as file:
    content = file.read()

print(content)