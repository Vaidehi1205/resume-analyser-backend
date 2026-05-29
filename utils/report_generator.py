from fpdf import FPDF
import os

REPORT_DIR = "reports"

os.makedirs(
    REPORT_DIR,
    exist_ok=True
)

def generate_pdf_report(
    score,
    similarity,
    resume_skills,
    jd_skills,
    matched_skills,
    missing_skills,
    chart_path,
    file_id
):

    pdf = FPDF()

    pdf.add_page()

    # ==========================================
    # TITLE
    # ==========================================

    pdf.set_font(
        "Arial",
        "B",
        18
    )

    pdf.cell(
        200,
        10,
        txt="AI Resume Analysis Report",
        ln=True,
        align="C"
    )

    pdf.ln(10)

    # ==========================================
    # SCORE
    # ==========================================

    pdf.set_font(
        "Arial",
        "B",
        14
    )

    pdf.cell(
        200,
        10,
        txt=f"Match Score: {round(score, 2)}%",
        ln=True
    )

    pdf.cell(
        200,
        10,
        txt=f"Semantic Similarity: {round(similarity * 100, 2)}%",
        ln=True
    )

    pdf.ln(5)

    # ==========================================
    # RESUME SKILLS
    # ==========================================

    pdf.set_font(
        "Arial",
        "B",
        12
    )

    pdf.cell(
        200,
        10,
        txt="Resume Skills:",
        ln=True
    )

    pdf.set_font(
        "Arial",
        "",
        11
    )

    pdf.multi_cell(
        0,
        8,
        txt=", ".join(resume_skills)
    )

    pdf.ln(4)

    # ==========================================
    # REQUIRED SKILLS
    # ==========================================

    pdf.set_font(
        "Arial",
        "B",
        12
    )

    pdf.cell(
        200,
        10,
        txt="Required Skills:",
        ln=True
    )

    pdf.set_font(
        "Arial",
        "",
        11
    )

    pdf.multi_cell(
        0,
        8,
        txt=", ".join(jd_skills)
    )

    pdf.ln(4)

    # ==========================================
    # MATCHED SKILLS
    # ==========================================

    pdf.set_font(
        "Arial",
        "B",
        12
    )

    pdf.cell(
        200,
        10,
        txt="Matched Skills:",
        ln=True
    )

    pdf.set_font(
        "Arial",
        "",
        11
    )

    pdf.multi_cell(
        0,
        8,
        txt=", ".join(matched_skills)
    )

    pdf.ln(4)

    # ==========================================
    # MISSING SKILLS
    # ==========================================

    pdf.set_font(
        "Arial",
        "B",
        12
    )

    pdf.cell(
        200,
        10,
        txt="Missing Skills:",
        ln=True
    )

    pdf.set_font(
        "Arial",
        "",
        11
    )

    if missing_skills:

        pdf.multi_cell(
            0,
            8,
            txt=", ".join(missing_skills)
        )

    else:

        pdf.multi_cell(
            0,
            8,
            txt="No missing skills found."
        )

    pdf.ln(10)

    # ==========================================
    # CHART
    # ==========================================

    if os.path.exists(chart_path):

        pdf.image(
            chart_path,
            x=30,
            w=150
        )

    # ==========================================
    # SAVE PDF
    # ==========================================

    report_filename = f"{file_id}.pdf"

    report_path = os.path.join(
        REPORT_DIR,
        report_filename
    )

    pdf.output(report_path)

    return report_filename
