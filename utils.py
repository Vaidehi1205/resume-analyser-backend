import PyPDF2
import os

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text


def load_resumes(resume_folder):
    resumes = []
    filenames = []

    for file in os.listdir(resume_folder):
        if file.endswith(".pdf"):
            path = os.path.join(resume_folder, file)
            text = extract_text_from_pdf(path)
            resumes.append(text)
            filenames.append(file)

    return resumes, filenames