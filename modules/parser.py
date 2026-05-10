import pdfplumber

import docx

import pytesseract

from PIL import Image

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


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
# IMAGE OCR PARSER
# =====================================================

def extract_text_from_image(image_file):

    image = Image.open(image_file)

    text = pytesseract.image_to_string(image)

    return text


# =====================================================
# UNIVERSAL PARSER
# =====================================================

def extract_resume_text(uploaded_file):

    file_name = uploaded_file.name.lower()

    # --------------------------------
    # PDF
    # --------------------------------

    if file_name.endswith(".pdf"):

        return extract_text_from_pdf(
            uploaded_file
        )

    # --------------------------------
    # DOCX
    # --------------------------------

    elif file_name.endswith(".docx"):

        return extract_text_from_docx(
            uploaded_file
        )

    # --------------------------------
    # IMAGE
    # --------------------------------

    elif file_name.endswith((".png", ".jpg", ".jpeg")):

        return extract_text_from_image(
            uploaded_file
        )

    else:

        return ""