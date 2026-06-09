import streamlit as st


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(

    page_title="AI Resume Analyzer",

    page_icon="📄",

    layout="wide"
)


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("📄 AI Resume Analyzer")

    st.markdown(
        """
        ### Modules

        🧠 Resume Analyzer  
        📊 Skill Analytics  
        💼 Job Intelligence  
        """
    )

    st.divider()

    st.info(
        "Navigate through modules using the sidebar."
    )


# =====================================================
# HERO SECTION
# =====================================================

st.markdown(
    """
    # 🚀 AI Resume Analyzer & Job Matcher

    An AI-powered platform for:

    - 📄 Resume Parsing
    - 🎯 ATS Analysis
    - 🧠 Career Role Prediction
    - 💼 Job Recommendations
    - 📊 Skill Market Analytics
    - 🤖 Semantic Matching with Transformers

    ---
    """
)


# =====================================================
# FEATURE CARDS
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        """
        ### 📄 Resume Analysis

        Analyze resumes using:
        - NLP
        - ATS scoring
        - semantic AI
        """
    )

with col2:

    st.markdown(
        """
        ### 🎯 Career Intelligence

        Predict:
        - career roles
        - skill gaps
        - learning recommendations
        """
    )

with col3:

    st.markdown(
        """
        ### 📊 Market Analytics

        Explore:
        - hiring trends
        - top skills
        - industry demand
        """
    )

st.divider()


# =====================================================
# TECH STACK
# =====================================================

st.subheader("🛠 Tech Stack")

tech_cols = st.columns(5)

tech_stack = [

    "Python",
    "Streamlit",
    "NLP",
    "Transformers",
    "Plotly"

]

for idx, tech in enumerate(tech_stack):

    with tech_cols[idx]:

        st.success(tech)


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Built using Python, Streamlit, NLP, and Transformer Embeddings 🚀"
)
