import streamlit as st
import os
import sys

# ----------------------------------------------------
# Add Project Root
# ----------------------------------------------------
BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# ----------------------------------------------------
# Import RAG
# ----------------------------------------------------
from llm.rag_chain import ask_legal_question

# ----------------------------------------------------
# Check Session
# ----------------------------------------------------
if "analysis_complete" not in st.session_state:
    st.session_state.analysis_complete = False

if not st.session_state.analysis_complete:
    st.warning("Please upload a document first.")
    st.stop()

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------
st.set_page_config(
    page_title="Legal FAQ",
    page_icon="❓",
    layout="wide"
)

st.title("❓ Ask Questions About Your Document")

st.markdown("---")

st.write(
    f"**Document:** {st.session_state.uploaded_file}"
)

st.write(
    f"**Document Type:** {st.session_state.document_type}"
)

st.write(
    f"**Language:** {st.session_state.language}"
)

st.markdown("---")

# ----------------------------------------------------
# Question
# ----------------------------------------------------
question = st.text_input(
    "Ask your legal question"
)

# ----------------------------------------------------
# Answer
# ----------------------------------------------------
if st.button("Get Answer"):

    if question.strip() == "":
        st.warning("Please enter a question.")

    else:

        with st.spinner("Searching legal document..."):

            answer = ask_legal_question(
                question,
                filename=st.session_state.uploaded_file,
                language=st.session_state.language,
                document_type=st.session_state.document_type
            )

        st.markdown("## AI Answer")

        st.success(answer)

st.markdown("---")

# ----------------------------------------------------
# Sample Questions
# ----------------------------------------------------
st.subheader("Example Questions")

st.info("""
• Explain this agreement.

• What are the tenant rights?

• What are my responsibilities?

• Explain Clause 5.

• Are there any risky clauses?

• What happens if I terminate the contract?

• Summarize this document.
""")

st.markdown("---")

# ----------------------------------------------------
# Navigation
# ----------------------------------------------------
col1, col2 = st.columns(2)

with col1:

    if st.button("⬅ Back to Analysis"):

        st.switch_page("pages/analysis.py")

with col2:

    if st.button("Next ➜ Rights"):

        st.switch_page("pages/rights.py")