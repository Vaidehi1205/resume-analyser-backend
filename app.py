from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import shutil
import os

from utils import extract_text_from_pdf
from services.scoring_service import compute_scores

app = FastAPI(title="AI Resume Screening API")

# CORS (for frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploaded_resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.post("/rank-resumes/")
async def rank_resumes(
    job_description: str = Form(...),
    files: List[UploadFile] = File(...)
):
    results = []

    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text from PDF
        resume_text = extract_text_from_pdf(file_path)

        # Compute scores
        scores = compute_scores(job_description, resume_text)

        results.append({
            "candidate": file.filename,
            "similarity_score": scores.get("similarity_score", 0),
            "skill_match_percent": scores.get("skill_match_percent", 0),
            "matched_skills": scores.get("matched_skills", []),
            "experience_relevance": scores.get("experience_relevance", 0),
            "final_score": scores.get("final_score", 0),
        })

    # Sort by final score
    ranked = sorted(
        results,
        key=lambda x: x["final_score"],
        reverse=True
    )

    return {
        "top_candidates": ranked[:3],
        "all_candidates": ranked
    }