# =====================================================
# SMART RESUME SECTION DETECTOR
# =====================================================

def extract_resume_sections(text):

    # -------------------------------------------------
    # SECTION HEADINGS
    # -------------------------------------------------

    headings = {

        "education": [
            "education",
            "academic background",
            "qualification"
        ],

        "experience": [
            "experience",
            "work experience",
            "employment",
            "internship"
        ],

        "projects": [
            "projects",
            "project"
        ],

        "skills": [
            "skills",
            "technical skills",
            "technologies"
        ],

        "certifications": [
            "certifications",
            "certificates"
        ]

    }

    # -------------------------------------------------
    # SPLIT INTO LINES
    # -------------------------------------------------

    lines = text.splitlines()

    # remove empty lines
    lines = [line.strip() for line in lines if line.strip()]

    # -------------------------------------------------
    # STORAGE
    # -------------------------------------------------

    sections = {

        "education": [],

        "experience": [],

        "projects": [],

        "skills": [],

        "certifications": []

    }

    current_section = None

    # -------------------------------------------------
    # PROCESS LINE BY LINE
    # -------------------------------------------------

    for line in lines:

        line_lower = line.lower()

        # ---------------------------------------------
        # DETECT SECTION
        # ---------------------------------------------

        found_heading = False

        for section, keywords in headings.items():

            if any(keyword == line_lower for keyword in keywords):

                current_section = section

                found_heading = True

                break

        # ---------------------------------------------
        # ADD CONTENT
        # ---------------------------------------------

        if not found_heading and current_section:

            sections[current_section].append(line)

    # -------------------------------------------------
    # JOIN CONTENT
    # -------------------------------------------------

    for section in sections:

        sections[section] = "\n".join(
            sections[section]
        )

    return sections