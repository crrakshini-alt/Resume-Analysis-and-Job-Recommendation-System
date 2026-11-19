
from pypdf import PdfReader
from docx import Document
from pathlib import Path


def extract_resume_text(file_path):

    file_path = Path(file_path)
    extension = file_path.suffix.lower()

    extracted_text = ""

    if extension == ".pdf":

        reader = PdfReader(file_path)

        for page_number, page in enumerate(reader.pages, start=1):

            page_text = page.extract_text()

            if page_text:
                extracted_text += page_text + "\n"

    elif extension == ".docx":

        document = Document(file_path)

        for paragraph in document.paragraphs:

            if paragraph.text.strip():
                extracted_text += paragraph.text + "\n"

        for table in document.tables:

            for row in table.rows:

                extracted_text += " | ".join(
                    cell.text.strip() for cell in row.cells
                ) + "\n"

    else:
        raise ValueError("Only PDF and DOCX files are supported.")

    if not extracted_text.strip():
        raise ValueError("No readable text found in the resume.")

    return extracted_text


if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent.parent

    resume_path = BASE_DIR / "resumes" / "sample_resume.pdf"

    if resume_path.exists():

        text = extract_resume_text(resume_path)

        print("\n========== EXTRACTED RESUME TEXT ==========")

        print(text)

    else:

        print("Resume file not found!")
        print("Please add a PDF or DOCX resume inside the resumes folder.")
