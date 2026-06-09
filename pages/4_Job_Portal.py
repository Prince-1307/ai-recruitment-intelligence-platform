import streamlit as st
import pandas as pd
import os

from modules.extractor import extract_skills
from modules.update_skills import update_skills
from modules.update_roles import update_roles

import ast
import pickle

from modules.parser import extract_resume_text
from modules.resume_analyzer import analyze_resume

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(

    page_title="Recruiter Dashboard",

    page_icon="💼",

    layout="wide"
)


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("💼 Recruiter Dashboard")

    st.markdown(
        """
        ### Features

        ✅ Post Jobs  
        ✅ AI Skill Extraction  
        ✅ Dynamic Skill Expansion  
        ✅ Role Management  
        ✅ Dataset Growth  
        """
    )

    st.divider()

    st.info(
        "Post jobs and expand the AI recruitment ecosystem."
    )


# =====================================================
# HERO SECTION
# =====================================================

st.markdown(
    """
    # 💼 AI Recruitment Job Portal

    Recruiters can:
    - post new jobs
    - add hiring requirements
    - use AI-powered skill extraction
    - dynamically improve the platform

    ---
    """
)


# =====================================================
# JOB FORM
# =====================================================

st.subheader("📝 Post a New Job")


with st.form("job_form"):

    # -------------------------------------------------
    # BASIC DETAILS
    # -------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        title = st.text_input(
            "Job Title"
        )

        company = st.text_input(
            "Company Name"
        )

    with col2:

        location = st.text_input(
            "Location"
        )

        clean_title = st.text_input(
            "Basic Role Title"
        )

    # -------------------------------------------------
    # REQUIRED SKILLS
    # -------------------------------------------------

    required_skills = st.text_input(

        "Required Skills (comma separated)",

        placeholder="Python, SQL, AWS, TensorFlow"
    )

    # -------------------------------------------------
    # DESCRIPTION
    # -------------------------------------------------

    description = st.text_area(

        "Job Description",

        height=250
    )

    # -------------------------------------------------
    # SUBMIT BUTTON
    # -------------------------------------------------

    submitted = st.form_submit_button(
        "🚀 Post Job"
    )


# =====================================================
# PROCESS SUBMISSION
# =====================================================

if submitted:

    # -------------------------------------------------
    # VALIDATION
    # -------------------------------------------------

    if not title or not description:

        st.error(
            "Please fill all required fields."
        )

    else:

        # =================================================
        # MANUAL SKILLS
        # =================================================

        manual_skills = [

            skill.strip().lower()

            for skill in required_skills.split(",")

            if skill.strip()
        ]

        # =================================================
        # AI SKILL EXTRACTION
        # =================================================

        ai_skills = extract_skills(
            description
        )

        # =================================================
        # COMBINED SKILLS
        # =================================================

        combined_skills = list(

            set(ai_skills + manual_skills)

        )

        # =================================================
        # UPDATE GLOBAL SKILLS
        # =================================================

        update_skills(
            combined_skills
        )

        # =================================================
        # UPDATE ROLE DATABASE
        # =================================================

        update_roles(
            clean_title
        )

        # =================================================
        # JOB DATAFRAME
        # =================================================

        new_job = pd.DataFrame([{

            "title": title,

            "company": company,

            "location": location,

            "clean_title": clean_title,

            "description": description,

            "skills": str(combined_skills)

        }])

        # =================================================
        # SAVE TO DATASET
        # =================================================

        dataset_path = (
            r"data/cleaned_job_postings.csv"
        )

        if os.path.exists(dataset_path):

            old_df = pd.read_csv(
                dataset_path
            )

            updated_df = pd.concat(

                [old_df, new_job],

                ignore_index=True
            )

            updated_df.to_csv(

                dataset_path,

                index=False
            )

        else:

            new_job.to_csv(

                dataset_path,

                index=False
            )

        # =================================================
        # SUCCESS MESSAGE
        # =================================================

        st.success(
            "✅ Job posted successfully!"
        )

        st.divider()

        # =================================================
        # JOB PREVIEW
        # =================================================

        st.subheader("📄 Job Preview")

        st.markdown(
            f"""
            <div style="
                border:1px solid #2d3748;
                border-radius:15px;
                padding:25px;
                background-color:#111827;
                margin-bottom:20px;
            ">

            <h2>{title}</h2>

            <p><b>Company:</b> {company}</p>

            <p><b>Location:</b> {location}</p>

            <p><b>Role Category:</b> {clean_title}</p>

            </div>
            """,

            unsafe_allow_html=True
        )

        st.write(description)

        st.divider()

        # =================================================
        # EXTRACTED SKILLS
        # =================================================

        st.subheader("🧠 Extracted & Required Skills")

        cols = st.columns(3)

        for idx, skill in enumerate(
            combined_skills
        ):

            with cols[idx % 3]:

                st.markdown(
                    f"""
                    <div style="
                        background-color:#15803d;
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


# =====================================================
# RECENT JOBS
# =====================================================


st.divider()

st.subheader("📌 Recently Added Jobs")

role_model = pickle.load(open(r"models/role_predictor.pkl", "rb"))


dataset_path = r"data/cleaned_job_postings.csv"

if os.path.exists(dataset_path):

    recent_jobs = pd.read_csv(
        dataset_path
    ).tail(5)

    recent_jobs = recent_jobs.iloc[::-1]

    for idx, row in recent_jobs.iterrows():

        with st.expander(
            f"💼 {row['title']} | {row['company']}"
        ):

            st.markdown(
                f"""
                ### {row['title']}

                **Company:** {row['company']}

                **Location:** {row['location']}

                **Role:** {row['clean_title']}
                """
            )

            st.write(row['description'])

            st.divider()

            # =============================================
            # JOB SKILLS
            # =============================================

            job_skills = ast.literal_eval(
                row['skills']
            )

            st.subheader("🧠 Required Skills")

            cols = st.columns(3)

            for i, skill in enumerate(job_skills):

                with cols[i % 3]:

                    st.markdown(
                        f"""
                        <div style="
                            background-color:#1d4ed8;
                            padding:10px;
                            border-radius:10px;
                            text-align:center;
                            margin-bottom:10px;
                            color:white;
                        ">
                            {skill}
                        </div>
                        """,

                        unsafe_allow_html=True
                    )

            st.divider()

            # =============================================
            # APPLICANT ANALYSIS
            # =============================================

            st.subheader(
                "📤 Upload Applicant Resume"
            )

            applicant_resume = st.file_uploader(

                "Upload Resume",

                type=["pdf","docx"],

                key=f"resume_{idx}"
            )

            # =============================================
            # PROCESS APPLICANT
            # =============================================

            if applicant_resume:

                # -----------------------------------------
                # EXTRACT TEXT
                # -----------------------------------------

                applicant_text = extract_resume_text(
                    applicant_resume
                )

                # -----------------------------------------
                # EXTRACT SKILLS
                # -----------------------------------------

                applicant_skills = extract_skills(
                    applicant_text
                )

                # -----------------------------------------
                # ATS ANALYSIS
                # -----------------------------------------

                resume_set = set(

                    [s.lower() for s in applicant_skills]

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

                # -----------------------------------------
                # ROLE PREDICTION
                # -----------------------------------------

                role_prediction = role_model.predict(
                    [applicant_text]
                )[0]

                # =========================================
                # ANALYSIS OUTPUT
                # =========================================

                st.success(
                    "✅ Resume analyzed successfully!"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(

                        "🎯 ATS Match Score",

                        f"{ats_score:.2f}%"

                    )

                with col2:

                    st.metric(

                        "🧠 Predicted Role",

                        role_prediction
                    )

                st.divider()

                # =========================================
                # MATCHED / MISSING SKILLS
                # =========================================

                col1, col2 = st.columns(2)

                with col1:

                    st.subheader(
                        "✅ Matched Skills"
                    )

                    for skill in matched:

                        st.success(skill)

                with col2:

                    st.subheader(
                        "⚠ Missing Skills"
                    )

                    for skill in missing:

                        st.warning(skill)

                st.divider()

                # =========================================
                # RESUME FEEDBACK
                # =========================================

                applicant_analysis = analyze_resume(

                    applicant_text,

                    applicant_skills
                )

                st.subheader(
                    "📊 Resume Quality"
                )

                st.metric(

                    "Resume Strength",

                    f"{applicant_analysis['resume_strength_score']}/100"
                )

if os.path.exists(dataset_path):

    recent_jobs = pd.read_csv(
        dataset_path
    ).tail(5)

    recent_jobs = recent_jobs.iloc[::-1]

    recent_jobs = recent_jobs.reset_index(
        drop=True
    )

    for idx, row in recent_jobs.iterrows():

        with st.expander(
            f"💼 {row['title']} | {row['company']}"
        ):

            st.markdown(
                f"""
                ### {row['title']}

                **Company:** {row['company']}

                **Location:** {row['location']}

                **Role:** {row['clean_title']}
                """
            )

            st.write(row['description'])

            st.divider()

            # =============================================
            # JOB SKILLS
            # =============================================

            job_skills = ast.literal_eval(
                row['skills']
            )

            st.subheader("🧠 Required Skills")

            cols = st.columns(3)

            for i, skill in enumerate(job_skills):

                with cols[i % 3]:

                    st.markdown(
                        f"""
                        <div style="
                            background-color:#1d4ed8;
                            padding:10px;
                            border-radius:10px;
                            text-align:center;
                            margin-bottom:10px;
                            color:white;
                        ">
                            {skill}
                        </div>
                        """,

                        unsafe_allow_html=True
                    )

            st.divider()

            # =============================================
            # APPLICANT ANALYSIS
            # =============================================

            st.subheader(
                "📤 Upload Applicant Resume"
            )

            applicant_resume = st.file_uploader(

                "Upload Resume",

                type=["pdf","docx"],

                key=f"resume_{idx}"
            )

            # =============================================
            # PROCESS APPLICANT
            # =============================================

            if applicant_resume:

                # -----------------------------------------
                # EXTRACT TEXT
                # -----------------------------------------

                applicant_text = extract_resume_text(
                    applicant_resume
                )

                # -----------------------------------------
                # EXTRACT SKILLS
                # -----------------------------------------

                applicant_skills = extract_skills(
                    applicant_text
                )

                # -----------------------------------------
                # ATS ANALYSIS
                # -----------------------------------------

                resume_set = set(

                    [s.lower() for s in applicant_skills]

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

                # -----------------------------------------
                # ROLE PREDICTION
                # -----------------------------------------

                role_prediction = role_model.predict(
                    [applicant_text]
                )[0]

                # =========================================
                # ANALYSIS OUTPUT
                # =========================================

                st.success(
                    "✅ Resume analyzed successfully!"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(

                        "🎯 ATS Match Score",

                        f"{ats_score:.2f}%"

                    )

                with col2:

                    st.metric(

                        "🧠 Predicted Role",

                        role_prediction
                    )

                st.divider()

                # =========================================
                # MATCHED / MISSING SKILLS
                # =========================================

                col1, col2 = st.columns(2)

                with col1:

                    st.subheader(
                        "✅ Matched Skills"
                    )

                    for skill in matched:

                        st.success(skill)

                with col2:

                    st.subheader(
                        "⚠ Missing Skills"
                    )

                    for skill in missing:

                        st.warning(skill)

                st.divider()

                # =========================================
                # RESUME FEEDBACK
                # =========================================

                applicant_analysis = analyze_resume(

                    applicant_text,

                    applicant_skills
                )

                st.subheader(
                    "📊 Resume Quality"
                )

                st.metric(

                    "Resume Strength",

                    f"{applicant_analysis['resume_strength_score']}/100"
                )
# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "AI-powered recruitment ecosystem 🚀"
)