import streamlit as st
import os
import sys

# --------------------------------------------------
# Add Project Root
# --------------------------------------------------
BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# --------------------------------------------------
# Import Risk Agent
# --------------------------------------------------
from agents.risk_flagging_agent import flag_risks

# --------------------------------------------------
# Check Session
# --------------------------------------------------
if "analysis_complete" not in st.session_state:
    st.session_state.analysis_complete = False

if not st.session_state.analysis_complete:
    st.warning("Please upload a document first.")
    st.stop()

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Risk Analysis",
    page_icon="⚠️",
    layout="wide"
)

st.title("⚠️ Risk Analysis")

st.markdown("---")

# --------------------------------------------------
# Document Information
# --------------------------------------------------
st.subheader("Uploaded Document")

st.write("**File Name:**", st.session_state.uploaded_file)

st.write("**Document Type:**", st.session_state.document_type)

st.write("**Language:**", st.session_state.language)

st.markdown("---")

# --------------------------------------------------
# Risk Analysis
# --------------------------------------------------
if st.button("Analyze Risks"):

    with st.spinner("Finding risky clauses..."):

        risks = flag_risks(
            st.session_state.document_text
        )

        st.session_state.risks = risks

# --------------------------------------------------
# Display Risks
# --------------------------------------------------
if "risks" in st.session_state:

    st.subheader("Risk Report")

    st.warning(st.session_state.risks)

st.markdown("---")

# --------------------------------------------------
# Risk Level
# --------------------------------------------------
if "risks" in st.session_state:

    st.subheader("Risk Level")

    risk_text = st.session_state.risks.lower()

    if "high" in risk_text:

        st.error("🔴 High Risk")

    elif "medium" in risk_text:

        st.warning("🟠 Medium Risk")

    else:

        st.success("🟢 Low Risk")

st.markdown("---")

# --------------------------------------------------
# Navigation
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:

    if st.button("⬅ Back to Rights"):

        st.switch_page("pages/rights.py")

with col2:

    if st.button("Next ➜ Recommendations"):

        st.switch_page("pages/next_steps.py")