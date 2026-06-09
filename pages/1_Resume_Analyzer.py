import streamlit as st
import pandas as pd
import ast
import pickle
import os

from modules.parser import extract_resume_text
from modules.extractor import extract_skills
from modules.resume_analyzer import analyze_resume
from modules.semantic_matcher import semantic_job_match
from modules.learning_resources import LEARNING_RESOURCES
from modules.pdf_report import generate_pdf_report


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(

    page_title="AI Resume Analyzer",

    page_icon="📄",

    layout="wide"
)


# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv(r"data/cleaned_job_postings.csv")


# =====================================================
# LOAD ROLE PREDICTOR
# =====================================================

role_model = pickle.load(open(r"models/role_predictor.pkl", "rb"))


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("📄 AI Resume Analyzer")

    st.markdown(
        """
        ### Features

        ✅ Resume Parsing
        ✅ ATS Analysis  
        ✅ Semantic Matching  
        ✅ Role Prediction  
        ✅ Skill Analytics  
        """
    )

    st.divider()

    st.info(
        "Upload your resume to receive AI-powered career insights."
    )


# =====================================================
# HERO SECTION
# =====================================================

st.markdown(
    """
    # 📄 AI Resume Analyzer & Job Matcher

    Analyze resumes using NLP and transformer-based semantic matching.

    ### Features:
    - 🎯 ATS Score
    - 🧠 Career Prediction
    - 💼 Job Recommendations
    - 📚 Skill Gap Analysis
    """
)

st.divider()


# =====================================================
# FILE UPLOADER
# =====================================================

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=[
    "pdf",
    "docx"
]
)


# =====================================================
# MAIN PIPELINE
# =====================================================

if uploaded_file:

    # -------------------------------------------------
    # EXTRACT RESUME TEXT
    # -------------------------------------------------

    resume_text = extract_resume_text(
        uploaded_file
    )

    # -------------------------------------------------
    # EXTRACT SKILLS
    # -------------------------------------------------

    resume_skills = extract_skills(
        resume_text
    )

    # -------------------------------------------------
    # RESUME ANALYSIS
    # -------------------------------------------------

    resume_analysis = analyze_resume(

        resume_text,

        resume_skills

    )

    # -------------------------------------------------
    # ROLE PREDICTION
    # -------------------------------------------------

    role_probabilities = role_model.predict_proba(
        [resume_text]
    )[0]

    role_labels = role_model.classes_

    role_df = pd.DataFrame({

        'Role': role_labels,

        'Probability': role_probabilities

    })

    role_df = role_df.sort_values(

        by='Probability',

        ascending=False

    )

    top_roles = role_df.head(3)

    # -------------------------------------------------
    # SEMANTIC MATCHING
    # -------------------------------------------------

    similarity_scores = semantic_job_match(
        df,
        resume_text

    )

    df['match_score'] = similarity_scores * 100

    top_jobs = df.sort_values(

        by='match_score',

        ascending=False

    ).head(3)

    # =================================================
    # RESUME STRENGTH ANALYSIS
    # =================================================

    with st.container():

        st.subheader("📊 Resume Strength Analysis")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(

                "Resume Strength",

                f"{resume_analysis['resume_strength_score']}/100"

            )

        with col2:

            st.metric(

                "Word Count",

                resume_analysis['word_count']

            )

        with col3:

            st.metric(

                "Skills Found",

                resume_analysis['skill_count']

            )

    st.divider()

    # =================================================
    # ROLE PREDICTION
    # =================================================

    with st.container():

        st.subheader("🎯 Predicted Career Roles")

        medals = ["🥇", "🥈", "🥉"]

        cols = st.columns(3)

        for idx, (_, row) in enumerate(
            top_roles.iterrows()
        ):

            probability = row['Probability'] * 100

            with cols[idx]:

                st.markdown(
                    f"""
                    ### {medals[idx]} {row['Role']}
                    """
                )

                st.metric(

                    label="Match Confidence",

                    value=f"{probability:.2f}%"

                )

                st.progress(
                    min(int(probability), 100)
                )

    st.divider()

    # =================================================
    # RESUME FEEDBACK
    # =================================================

    with st.container():

        st.subheader("📝 Resume Feedback")

        if resume_analysis['has_projects']:

            st.success("✔ Projects section detected")

        else:

            st.warning("⚠ Add projects section")

        if resume_analysis['has_experience']:

            st.success("✔ Experience section detected")

        else:

            st.warning("⚠ Add internship/work experience")

        if resume_analysis['has_education']:

            st.success("✔ Education section detected")

        else:

            st.warning("⚠ Add education details")

        if resume_analysis['word_count'] < 250:

            st.warning(
                "⚠ Resume content seems too short"
            )

        else:

            st.success(
                "✔ Resume length looks good"
            )

    st.divider()

    # =================================================
    # EXTRACTED SKILLS
    # =================================================

    with st.container():

        st.subheader("🧠 Extracted Skills")

        cols = st.columns(3)

        for idx, skill in enumerate(resume_skills):

            with cols[idx % 3]:

                st.markdown(
                    f"""
                    <div style="
                        background-color:#335db0;
                        padding:10px;
                        border-radius:12px;
                        text-align:center;
                        margin-bottom:10px;
                        color:white;
                        font-size:15px;
                        font-weight:500;
                    ">
                        {skill}
                    </div>
                    """,

                    unsafe_allow_html=True
                )

    st.divider()

    # =================================================
    # JOB RECOMMENDATIONS
    # =================================================

    st.subheader("💼 Top Recommended Jobs")

    best_ats_score = 0
    best_matched = set()
    best_missing = set()

    for idx, (_, row) in enumerate(
        top_jobs.iterrows()
    ):

        st.markdown(
            f"""
            <div style="
                border:1px solid #2d3748;
                border-radius:15px;
                padding:20px;
                margin-bottom:20px;
                background-color:#111827;
            ">

            <h2>{row['title']}</h2>

            <p><b>Company:</b> {row['company']}</p>

            <p><b>Location:</b> {row['location']}</p>

            <p><b>Match Score:</b> {row['match_score']:.2f}%</p>

            </div>
            """,

            unsafe_allow_html=True
        )

        # -------------------------------------------------
        # ATS ANALYSIS
        # -------------------------------------------------

        job_skills = ast.literal_eval(
            row['skills']
        )

        resume_set = set(
            [s.lower() for s in resume_skills]
        )

        job_set = set(
            [s.lower() for s in job_skills]
        )

        matched = resume_set.intersection(
            job_set
        )

        missing = job_set.difference(
            resume_set
        )

        ats_score = (

            len(matched)

            / len(job_set)

        ) * 100 if len(job_set) > 0 else 0

        # SAVE BEST MATCH
        if idx == 0:

            best_ats_score = ats_score

            best_matched = matched

            best_missing = missing

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(

                "ATS Score",

                f"{ats_score:.2f}%"

            )

        with col2:

            st.write("✅ Matched Skills")

            st.write(list(matched))

        with col3:

            st.write("⚠ Missing Skills")

            st.write(list(missing))

        # -------------------------------------------------
        # LEARNING RECOMMENDATIONS
        # -------------------------------------------------

        learning_recommendations = {}

        for skill in missing:

            if skill in LEARNING_RESOURCES:

                learning_recommendations[skill] = (

                    LEARNING_RESOURCES[skill]

                )

        if learning_recommendations:

            st.subheader("📚 Suggested Learning")

            for skill, course in learning_recommendations.items():

                st.markdown(
                    f"""
                    - **{skill.title()}**
                      → {course}
                    """
                )

        st.divider()

    # =====================================================
    # GENERATE PDF REPORT
    # =====================================================

    generate_pdf_report(

        r"reports/resume_report.pdf",

        best_ats_score,

        top_roles,

        resume_skills,

        best_matched,

        best_missing

    )

    # =====================================================
    # DOWNLOAD REPORT
    # =====================================================

    st.subheader("📄 Download ATS Report")

    with open(
        r"reports/resume_report.pdf",
        "rb"
    ) as pdf_file:

        st.download_button(

            label="⬇ Download Professional Report",

            data=pdf_file,

            file_name="ATS_Report.pdf",

            mime="application/pdf"
        )

    st.divider()

    # =====================================================
    # SAVE HISTORY
    # =====================================================

    history_entry = pd.DataFrame([{

        "Resume": uploaded_file.name,

        "ATS Score": round(best_ats_score, 2),

        "Top Role": top_roles.iloc[0]['Role']

    }])


    # -----------------------------------------------------
    # CREATE / APPEND CSV
    # -----------------------------------------------------

    if os.path.exists(r"data/resume_history.csv"):

        old_history = pd.read_csv(
            r"data/resume_history.csv"
        )

        updated_history = pd.concat(

            [old_history, history_entry],

            ignore_index=True
        )

        # remove duplicates
        updated_history = updated_history.drop_duplicates()

        updated_history.to_csv(

            r"data/resume_history.csv",

            index=False
        )

    else:

        history_entry.to_csv(

            r"data/resume_history.csv",

            index=False
        )


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Built with Python, Streamlit, NLP, and Transformer Embeddings 🚀"
)
