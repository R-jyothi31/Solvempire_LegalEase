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
# Import Agent
# --------------------------------------------------
from agents.next_steps_agent import suggest_next_steps

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
    page_title="Legal Recommendations",
    page_icon="✅",
    layout="wide"
)

st.title("✅ Legal Recommendations")

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
# AI Recommendations
# --------------------------------------------------
if st.button("Generate Recommendations"):

    with st.spinner("Generating legal recommendations..."):

        recommendations = suggest_next_steps(
            st.session_state.document_text
        )

        st.session_state.next_steps = recommendations

# --------------------------------------------------
# Display Recommendations
# --------------------------------------------------
if "next_steps" in st.session_state:

    st.subheader("AI Recommendations")

    st.success(st.session_state.next_steps)

st.markdown("---")

# --------------------------------------------------
# Summary
# --------------------------------------------------
st.subheader("Document Summary")

st.info(f"""
**Document Name:** {st.session_state.uploaded_file}

**Document Type:** {st.session_state.document_type}

**Language:** {st.session_state.language}

**Total Clauses:** {len(st.session_state.clauses)}
""")

st.markdown("---")

# --------------------------------------------------
# Navigation
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:

    if st.button("⬅ Back to Risk Analysis"):

        st.switch_page("pages/risk.py")

with col2:

    if st.button("Analyze Another Document"):

        # Clear Session State
        for key in list(st.session_state.keys()):
            del st.session_state[key]

        st.switch_page("pages/upload.py")