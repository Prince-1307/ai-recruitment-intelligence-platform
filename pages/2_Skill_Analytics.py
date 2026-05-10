import streamlit as st
import pandas as pd
import ast

from collections import Counter

import plotly.express as px


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(

    page_title="Skill Analytics",

    page_icon="📊",

    layout="wide"
)


# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv(
    r"data\cleaned_job_postings.csv"
)


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("📊 Skill Analytics")

    st.markdown(
        """
        ### Dashboard Insights

        🔥 Top Skills  
        💼 Hiring Roles  
        📍 Hiring Locations  
        📈 Market Trends  
        """
    )

    st.divider()

    st.info(
        "Explore real-world hiring insights extracted from job postings."
    )


# =====================================================
# HERO SECTION
# =====================================================

st.markdown(
    """
    # 📊 Skill Analytics Dashboard

    Analyze:
    - in-demand skills
    - hiring trends
    - top career roles
    - market intelligence

    ---
    """
)


# =====================================================
# CLEAN SKILLS COLUMN
# =====================================================

df['skills'] = df['skills'].apply(
    ast.literal_eval
)


# =====================================================
# FLATTEN SKILLS
# =====================================================

all_skills = []

for skills in df['skills']:

    all_skills.extend(skills)


# =====================================================
# SKILL COUNTS
# =====================================================

skill_counts = Counter(all_skills)

top_skills = pd.DataFrame(

    skill_counts.most_common(15),

    columns=['Skill', 'Count']

)


# =====================================================
# REMOVE "OTHER"
# =====================================================

filtered_roles = df[
    df['clean_title'] != "Other"
]


# =====================================================
# TOP ROLES
# =====================================================

top_roles = filtered_roles[
    'clean_title'
].value_counts().head(10)


# =====================================================
# TOP LOCATIONS
# =====================================================

top_locations = df[
    'location'
].value_counts().head(10)


# =====================================================
# METRICS SECTION
# =====================================================

st.subheader("📌 Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "📄 Total Jobs",
        len(df)
    )

with col2:

    st.metric(
        "🧠 Unique Skills",
        len(skill_counts)
    )

with col3:

    st.metric(
        "💼 Unique Roles",
        filtered_roles['clean_title'].nunique()
    )

st.divider()


# =====================================================
# TOP SKILLS SECTION
# =====================================================

with st.container():

    st.subheader("🔥 Top In-Demand Skills")

    fig = px.bar(

        top_skills,

        x='Skill',

        y='Count',

        text='Count',

        title='Top In-Demand Skills'
    )

    fig.update_layout(

        xaxis_title="Skills",

        yaxis_title="Frequency"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()


# =====================================================
# TOP ROLES SECTION
# =====================================================

with st.container():

    st.subheader("💼 Most Common Hiring Roles")

    role_df = pd.DataFrame({

        'Role': top_roles.index,

        'Count': top_roles.values

    })

    role_fig = px.bar(

        role_df,

        x='Role',

        y='Count',

        text='Count',

        title='Top Hiring Roles'
    )

    role_fig.update_layout(

        xaxis_title="Roles",

        yaxis_title="Frequency"
    )

    st.plotly_chart(
        role_fig,
        use_container_width=True
    )

st.divider()


# =====================================================
# SKILL DISTRIBUTION
# =====================================================

with st.container():

    st.subheader("📈 Skill Distribution")

    pie_fig = px.pie(

        top_skills.head(10),

        names='Skill',

        values='Count',

        title='Top Skill Distribution'
    )

    st.plotly_chart(
        pie_fig,
        use_container_width=True
    )

st.divider()


# =====================================================
# LOCATION ANALYTICS
# =====================================================

with st.container():

    st.subheader("📍 Top Hiring Locations")

    location_df = pd.DataFrame({

        'Location': top_locations.index,

        'Count': top_locations.values

    })

    location_fig = px.bar(

        location_df,

        x='Location',

        y='Count',

        text='Count',

        title='Top Hiring Locations'
    )

    location_fig.update_layout(

        xaxis_title="Locations",

        yaxis_title="Jobs"
    )

    st.plotly_chart(
        location_fig,
        use_container_width=True
    )

st.divider()


# =====================================================
# MARKET INSIGHTS
# =====================================================

with st.container():

    st.subheader("🧠 Market Insights")

    most_demanded_skill = top_skills.iloc[0]['Skill']

    most_common_role = top_roles.index[0]

    top_location = top_locations.index[0]

    st.success(
        f"🔥 Most demanded skill: {most_demanded_skill}"
    )

    st.success(
        f"💼 Most common role: {most_common_role}"
    )

    st.success(
        f"📍 Top hiring location: {top_location}"
    )

st.divider()


# =====================================================
# FOOTER
# =====================================================

st.caption(
    "AI-powered market analytics using real-world job data 🚀"
)