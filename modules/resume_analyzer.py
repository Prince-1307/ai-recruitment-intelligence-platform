import re


# =====================================================
# RESUME STRENGTH ANALYZER
# =====================================================

def analyze_resume(resume_text, resume_skills):

    analysis = {}

    # -------------------------------------------------
    # WORD COUNT
    # -------------------------------------------------

    words = resume_text.split()

    word_count = len(words)

    analysis['word_count'] = word_count

    # -------------------------------------------------
    # SKILL COUNT
    # -------------------------------------------------

    analysis['skill_count'] = len(resume_skills)

    # -------------------------------------------------
    # PROJECT SECTION
    # -------------------------------------------------

    has_projects = bool(

        re.search(
            r'project|projects',
            resume_text,
            re.IGNORECASE
        )
    )

    analysis['has_projects'] = has_projects

    # -------------------------------------------------
    # EXPERIENCE SECTION
    # -------------------------------------------------

    has_experience = bool(

        re.search(
            r'experience|internship|work experience',
            resume_text,
            re.IGNORECASE
        )
    )

    analysis['has_experience'] = has_experience

    # -------------------------------------------------
    # EDUCATION SECTION
    # -------------------------------------------------

    has_education = bool(

        re.search(
            r'education|university|college|bachelor|master',
            resume_text,
            re.IGNORECASE
        )
    )

    analysis['has_education'] = has_education

    # -------------------------------------------------
    # SCORE CALCULATION
    # -------------------------------------------------

    score = 0

    # word count
    if word_count >= 300:
        score += 20

    # skills
    if len(resume_skills) >= 5:
        score += 25

    # projects
    if has_projects:
        score += 20

    # experience
    if has_experience:
        score += 20

    # education
    if has_education:
        score += 15

    analysis['resume_strength_score'] = score

    return analysis