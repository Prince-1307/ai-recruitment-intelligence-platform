from reportlab.platypus import (

    SimpleDocTemplate,

    Paragraph,

    Spacer

)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib.pagesizes import letter


# =====================================================
# PDF REPORT GENERATOR
# =====================================================

def generate_pdf_report(

    file_path,

    ats_score,

    top_roles,

    resume_skills,

    matched_skills,

    missing_skills

):
    Path(file_path).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    doc = SimpleDocTemplate(

        file_path,

        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elements = []

    # -------------------------------------------------
    # TITLE
    # -------------------------------------------------

    title = Paragraph(

        "AI Resume Analysis Report",

        styles['Title']
    )

    elements.append(title)

    elements.append(Spacer(1, 20))

    # -------------------------------------------------
    # ATS SCORE
    # -------------------------------------------------

    ats = Paragraph(

        f"<b>ATS Score:</b> {ats_score:.2f}%",

        styles['BodyText']
    )

    elements.append(ats)

    elements.append(Spacer(1, 12))

    # -------------------------------------------------
    # TOP ROLES
    # -------------------------------------------------

    role_text = "<br/>".join([

        f"{row['Role']} → {row['Probability'] * 100:.2f}%"

        for _, row in top_roles.iterrows()

    ])

    roles = Paragraph(

        f"<b>Predicted Roles:</b><br/>{role_text}",

        styles['BodyText']
    )

    elements.append(roles)

    elements.append(Spacer(1, 12))

    # -------------------------------------------------
    # SKILLS
    # -------------------------------------------------

    skills = Paragraph(

        f"<b>Extracted Skills:</b><br/>"

        f"{', '.join(resume_skills)}",

        styles['BodyText']
    )

    elements.append(skills)

    elements.append(Spacer(1, 12))

    # -------------------------------------------------
    # MATCHED SKILLS
    # -------------------------------------------------

    matched = Paragraph(

        f"<b>Matched Skills:</b><br/>"

        f"{', '.join(matched_skills)}",

        styles['BodyText']
    )

    elements.append(matched)

    elements.append(Spacer(1, 12))

    # -------------------------------------------------
    # MISSING SKILLS
    # -------------------------------------------------

    missing = Paragraph(

        f"<b>Missing Skills:</b><br/>"

        f"{', '.join(missing_skills)}",

        styles['BodyText']
    )

    elements.append(missing)

    # -------------------------------------------------
    # BUILD PDF
    # -------------------------------------------------

    doc.build(elements)
