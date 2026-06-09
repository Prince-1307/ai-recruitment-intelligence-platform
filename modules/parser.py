import pdfplumber

import docx

# =====================================================
# PDF PARSER
# =====================================================

def extract_text_from_pdf(pdf_file):

    text = ""

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:

                text += extracted + "\n"

    return text


# =====================================================
# DOCX PARSER
# =====================================================

def extract_text_from_docx(docx_file):

    doc = docx.Document(docx_file)

    text = []

    for para in doc.paragraphs:

        text.append(para.text)

    return "\n".join(text)



# =====================================================
# UNIVERSAL PARSER
# =====================================================

def extract_resume_text(uploaded_file):

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)

    elif file_name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)

    else:
        raise ValueError(
            "Only PDF and DOCX files are supported."
        )