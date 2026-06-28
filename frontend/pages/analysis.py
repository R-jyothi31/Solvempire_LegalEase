import streamlit as st

# -----------------------------------------------------
# Check if document has been analyzed
# -----------------------------------------------------
if "analysis_complete" not in st.session_state:
    st.session_state.analysis_complete = False

if not st.session_state.analysis_complete:
    st.warning("Please upload a document first.")
    st.stop()

# -----------------------------------------------------
# Page Title
# -----------------------------------------------------
st.set_page_config(
    page_title="Document Analysis",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Document Analysis")

st.markdown("---")

# -----------------------------------------------------
# Document Information
# -----------------------------------------------------
col1, col2 = st.columns(2)

with col1:

    st.subheader("📁 File Information")

    st.write(
        "**Filename:**",
        st.session_state.uploaded_file
    )

    st.write(
        "**Document Type:**",
        st.session_state.document_type
    )

with col2:

    st.subheader("🌐 Language")

    st.write(
        st.session_state.language
    )

st.markdown("---")

# -----------------------------------------------------
# Extracted Text
# -----------------------------------------------------
st.subheader("📜 Extracted Text")

st.text_area(
    "Document Text",
    st.session_state.document_text,
    height=250
)

st.markdown("---")

# -----------------------------------------------------
# Extracted Clauses
# -----------------------------------------------------
st.subheader("📑 Extracted Clauses")

clauses = st.session_state.clauses

if len(clauses) == 0:

    st.info("No clauses found.")

else:

    for i, clause in enumerate(clauses, start=1):

        with st.expander(f"Clause {i}"):

            st.write(clause)

st.markdown("---")

# -----------------------------------------------------
# Summary
# -----------------------------------------------------
st.subheader("📋 Summary")

st.info(
    f"""
Document Type : {st.session_state.document_type}

Language : {st.session_state.language}

Total Clauses : {len(st.session_state.clauses)}
"""
)

st.markdown("---")

# -----------------------------------------------------
# Navigation Buttons
# -----------------------------------------------------
col1, col2 = st.columns(2)

with col1:

    if st.button("⬅ Back to Upload"):

        st.switch_page("pages/upload.py")

with col2:

    if st.button("Next ➜ FAQ"):

        st.switch_page("pages/faq.py")