from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form,
    HTTPException
)

from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import shutil
import uuid
import os
import logging
import traceback
import json

from utils.pdf_reader import extract_text_from_pdf
from utils.cleaner import clean_text
from utils.extractor import extract_skills
from utils.similarity import compute_similarity
from utils.scoring import calculate_match_score
from utils.charts import generate_chart
from utils.report_generator import generate_pdf_report

# =====================================================
# APP CONFIG
# =====================================================

app = FastAPI(
    title="AI Resume Analyzer API",
    version="2.0.0"
)

# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# LOGGING
# =====================================================

logging.basicConfig(level=logging.INFO)

# =====================================================
# DIRECTORIES
# =====================================================

UPLOAD_DIR = "uploads"
REPORT_DIR = "reports"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

os.makedirs(
    REPORT_DIR,
    exist_ok=True
)

# =====================================================
# LOAD LEARNING RESOURCES
# =====================================================

if os.path.exists("resources.json"):

    with open("resources.json", "r") as f:
        LEARNING_RESOURCES = json.load(f)

else:
    LEARNING_RESOURCES = {}

# =====================================================
# ROOT
# =====================================================

@app.get("/")
async def root():

    return {
        "message": "AI Resume Analyzer Running"
    }

# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/health")
async def health_check():

    return {
        "status": "healthy"
    }

# =====================================================
# ANALYZE
# =====================================================

@app.post("/analyze")
async def analyze_resume(
    job_description: str = Form(...),
    resume: UploadFile = File(...)
):

    try:

        # =================================================
        # VALIDATE FILE
        # =================================================

        if resume.content_type != "application/pdf":

            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed."
            )

        # =================================================
        # VALIDATE JD
        # =================================================

        if not job_description.strip():

            raise HTTPException(
                status_code=400,
                detail="Job Description cannot be empty."
            )

        # =================================================
        # SAVE PDF
        # =================================================

        file_id = str(uuid.uuid4())

        pdf_path = os.path.join(
            UPLOAD_DIR,
            f"{file_id}.pdf"
        )

        with open(pdf_path, "wb") as buffer:

            shutil.copyfileobj(
                resume.file,
                buffer
            )

        logging.info(f"PDF saved: {pdf_path}")

        # =================================================
        # EXTRACT TEXT
        # =================================================

        resume_text = extract_text_from_pdf(
            pdf_path
        )

        if not resume_text.strip():

            raise HTTPException(
                status_code=400,
                detail="No readable text found in PDF."
            )

        # =================================================
        # CLEAN TEXT
        # =================================================

        cleaned_resume = clean_text(
            resume_text
        )

        cleaned_jd = clean_text(
            job_description
        )


        # =================================================
        # SKILL EXTRACTION
        # =================================================

        resume_skills = extract_skills(
            cleaned_resume
        )

        jd_skills = extract_skills(
            cleaned_jd
        )

        # Remove duplicates

        resume_skills = list(
            set(resume_skills)
        )

        jd_skills = list(
            set(jd_skills)
        )

        # =================================================
        # MATCHED + MISSING
        # =================================================

        matched_skills = list(
            set(resume_skills).intersection(
                set(jd_skills)
            )
        )

        missing_skills = list(
            set(jd_skills) - set(resume_skills)
        )

        # =================================================
        # SEMANTIC SIMILARITY
        # =================================================

        similarity = compute_similarity(
            cleaned_resume,
            cleaned_jd
        )

        # =================================================
        # MATCH SCORE
        # =================================================

        score = calculate_match_score(
            similarity,
            matched_skills,
            len(jd_skills)
        )

        # =================================================
        # CHART
        # =================================================

        chart_path = generate_chart(
            matched=len(matched_skills),
            missing=len(missing_skills),
            score =  score,
            file_id=file_id
        )

        # =================================================
        # LEARNING RECOMMENDATIONS
        # =================================================

        recommendations = {}

        for skill in missing_skills:

            if skill in LEARNING_RESOURCES:

                recommendations[skill] = (
                    LEARNING_RESOURCES[skill]
                )

        # =================================================
        # PDF REPORT
        # =================================================

        report_filename = generate_pdf_report(
            score=score,
            similarity=similarity,
            resume_skills=resume_skills,
            jd_skills=jd_skills,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            chart_path=chart_path,
            file_id=file_id
        )

        logging.info(
            f"Analysis completed: {file_id}"
        )

        # =================================================
        # RESPONSE
        # =================================================

        return {

            "success": True,

            "message":
            "Resume analyzed successfully.",

            "match_score":
            round(score, 2),

            "semantic_similarity":
            round(similarity * 100, 2),

            "resume_skills":
            resume_skills,

            "required_skills":
            jd_skills,

            "matched_skills":
            matched_skills,

            "missing_skills":
            missing_skills,

            "recommendations":
            recommendations,

            "total_resume_skills":
            len(resume_skills),

            "total_required_skills":
            len(jd_skills),

            "pdf_report":
            report_filename,

            "download_url":
            f"http://localhost:8000/download/{report_filename}"
        }

    except HTTPException as e:

        raise e

    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# =====================================================
# DOWNLOAD REPORT
# =====================================================

@app.get("/download/{file_name}")
async def download_report(file_name: str):

    file_path = os.path.join(
        REPORT_DIR,
        file_name
    )

    if not os.path.exists(file_path):

        raise HTTPException(
            status_code=404,
            detail="Report not found."
        )

    return FileResponse(
        path=file_path,
        filename=file_name,
        media_type="application/pdf"
    )
