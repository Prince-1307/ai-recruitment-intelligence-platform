import streamlit as st
import pandas as pd
import plotly.express as px
import os


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(

    page_title="Resume History",

    page_icon="🕘",

    layout="wide"
)


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🕘 Resume History")

    st.markdown(
        """
        ### Features

        📄 Previous Uploads  
        🎯 ATS Tracking  
        🧠 Role History  
        📈 Progress Analytics  
        """
    )

    st.divider()

    st.info(
        "Track previous resume analyses and ATS performance."
    )


# =====================================================
# HERO SECTION
# =====================================================

st.markdown(
    """
    # 🕘 Resume Analysis History

    Track:
    - ATS progression
    - uploaded resumes
    - predicted career roles
    - performance trends

    ---
    """
)


# =====================================================
# CHECK HISTORY FILE
# =====================================================

if os.path.exists(r"data\resume_history.csv"):

    history_df = pd.read_csv(
        r"data\resume_history.csv"
    )

    # =================================================
    # METRICS
    # =================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "📄 Total Analyses",
            len(history_df)
        )

    with col2:

        st.metric(
            "🎯 Highest ATS Score",
            f"{history_df['ATS Score'].max():.2f}%"
        )

    with col3:

        st.metric(
            "🧠 Unique Roles",
            history_df['Top Role'].nunique()
        )

    st.divider()

    # =================================================
    # HISTORY TABLE
    # =================================================

    st.subheader("📋 Resume Analysis Records")

    st.dataframe(

        history_df,

        use_container_width=True
    )

    st.divider()

    # =================================================
    # ATS TREND CHART
    # =================================================

    st.subheader("📈 ATS Score Progression")

    trend_fig = px.line(

        history_df.reset_index(),

        x=history_df.index,

        y='ATS Score',

        markers=True,

        title='ATS Score Trend'
    )

    trend_fig.update_layout(

        xaxis_title="Analysis Number",

        yaxis_title="ATS Score"
    )

    st.plotly_chart(

        trend_fig,

        use_container_width=True
    )

    st.divider()

    # =================================================
    # ROLE DISTRIBUTION
    # =================================================

    st.subheader("🎯 Predicted Role Distribution")

    role_counts = history_df[
        'Top Role'
    ].value_counts()

    role_fig = px.pie(

        names=role_counts.index,

        values=role_counts.values,

        title='Career Role Distribution'
    )

    st.plotly_chart(

        role_fig,

        use_container_width=True
    )

    st.divider()

    # =================================================
    # DOWNLOAD HISTORY
    # =================================================

    csv_data = history_df.to_csv(
        index=False
    )

    st.download_button(

        label="⬇ Download History CSV",

        data=csv_data,

        file_name=r"data\resume_history.csv",

        mime="text/csv"
    )

else:

    st.warning(
        "No resume analysis history found yet."
    )


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "AI-powered resume tracking dashboard 🚀"
)