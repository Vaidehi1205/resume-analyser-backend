from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

import os

REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)

def generate_pdf_report(
    score,
    matched_skills,
    missing_skills,
    resume_skills,
    jd_skills,
    chart_path,
    file_id
):

    pdf_path = f"{REPORT_DIR}/{file_id}.pdf"

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elements = []

    # TITLE
    elements.append(
        Paragraph(
            "AI Resume Analysis Report",
            styles['Title']
        )
    )

    elements.append(Spacer(1, 20))

    # SCORE
    elements.append(
        Paragraph(
            f"<b>Match Score:</b> {score}%",
            styles['Heading2']
        )
    )

    elements.append(Spacer(1, 20))

    # CHART
    elements.append(
        Image(chart_path, width=300, height=300)
    )

    elements.append(Spacer(1, 20))

    # REQUIRED SKILLS
    elements.append(
        Paragraph(
            f"<b>Required Skills:</b> {', '.join(jd_skills)}",
            styles['BodyText']
        )
    )

    elements.append(Spacer(1, 12))

    # RESUME SKILLS
    elements.append(
        Paragraph(
            f"<b>Resume Skills:</b> {', '.join(resume_skills)}",
            styles['BodyText']
        )
    )

    elements.append(Spacer(1, 12))

    # MATCHED
    elements.append(
        Paragraph(
            f"<b>Matched Skills:</b> {', '.join(matched_skills)}",
            styles['BodyText']
        )
    )

    elements.append(Spacer(1, 12))

    # MISSING
    elements.append(
        Paragraph(
            f"<b>Missing Skills:</b> {', '.join(missing_skills)}",
            styles['BodyText']
        )
    )

    doc.build(elements)

    return pdf_path.split("/")[-1]