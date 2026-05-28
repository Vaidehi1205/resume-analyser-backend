from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import shutil
import uuid
import os

from utils.pdf_reader import extract_text_from_pdf
from utils.cleaner import clean_text
from utils.extractor import extract_skills
from utils.similarity import compute_similarity
from utils.scoring import calculate_match_score
from utils.charts import generate_chart
from utils.report_generator import generate_pdf_report

app = FastAPI()

UPLOAD_DIR = "uploads"
REPORT_DIR = "reports"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

@app.post("/analyze")
async def analyze_resume(
    job_description: str = Form(...),
    resume: UploadFile = File(...)
):

    # -----------------------------
    # SAVE PDF
    # -----------------------------

    file_id = str(uuid.uuid4())
    pdf_path = f"{UPLOAD_DIR}/{file_id}.pdf"

    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    # -----------------------------
    # EXTRACT TEXT
    # -----------------------------

    resume_text = extract_text_from_pdf(pdf_path)

    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(job_description)

    # -----------------------------
    # SKILLS
    # -----------------------------

    resume_skills = extract_skills(cleaned_resume)
    jd_skills = extract_skills(cleaned_jd)

    matched_skills = list(
        set(resume_skills).intersection(jd_skills)
    )

    missing_skills = list(
        set(jd_skills) - set(resume_skills)
    )

    # -----------------------------
    # SIMILARITY
    # -----------------------------

    similarity = compute_similarity(
        cleaned_resume,
        cleaned_jd
    )

    score = calculate_match_score(
        similarity,
        matched_skills,
        len(jd_skills)
    )

    # -----------------------------
    # CHART
    # -----------------------------

    chart_path = generate_chart(
        score,
        len(matched_skills),
        len(missing_skills),
        file_id
    )

    # -----------------------------
    # PDF REPORT
    # -----------------------------

    report_path = generate_pdf_report(
        score=score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        resume_skills=resume_skills,
        jd_skills=jd_skills,
        chart_path=chart_path,
        file_id=file_id
    )

    return {
        "match_score": score,
        "resume_skills": resume_skills,
        "required_skills": jd_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "pdf_report": report_path
    }


@app.get("/download/{file_name}")
async def download_report(file_name: str):

    file_path = f"reports/{file_name}"

    return FileResponse(
        path=file_path,
        filename=file_name,
        media_type='application/pdf'
    )