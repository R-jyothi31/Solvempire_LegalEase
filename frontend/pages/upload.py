import os
import sys
import streamlit as st

# ----------------------------------------------------
# Add Project Root
# ----------------------------------------------------
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# ----------------------------------------------------
# Imports
# ----------------------------------------------------
from rag.pdf_loader import extract_text
from rag.chunker import chunk_document
from rag.embedding import create_vector_store
from multilingual.language_detector import detect_language
from agents.document_parser import detect_document_type
from agents.clause_extractor import extract_clauses

# ----------------------------------------------------
# Upload Folder
# ----------------------------------------------------
UPLOAD_FOLDER = os.path.join(BASE_DIR, "data", "raw", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ----------------------------------------------------
# Upload Page
# ----------------------------------------------------
def upload_page():

    css_path = os.path.join(BASE_DIR, "frontend", "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # --------------------------------------------------
    # Extra page-level styles (next_steps palette)
    # --------------------------------------------------
    st.markdown("""
<style>
/* ── Page title ── */
h1 {
    font-family: 'Playfair Display', serif;
    color: #0D1B2A;
}
.page-subtitle {
    color: #718096;
    font-size: 0.95rem;
    margin-top: 0.2rem;
}

/* ── Section strip header ── */
.section-strip {
    background: linear-gradient(90deg, #0D1B2A 0%, #1B2E42 100%);
    color: #C9A84C;
    border-radius: 8px;
    padding: 0.6rem 1.2rem;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 1rem;
    margin-top: 1.5rem;
}

/* ── Summary panel (file list) ── */
.summary-panel {
    background: #FFFFFF;
    border: 1px solid #E2DAC8;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    box-shadow: 0 2px 10px rgba(13,27,42,0.06);
}
.summary-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.42rem 0;
    border-bottom: 1px solid #F5EDD6;
    font-size: 0.91rem;
    color: #0D1B2A;
}
.summary-row:last-child { border-bottom: none; }
.summary-key {
    color: #718096;
    font-weight: 500;
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.meta-value {
    color: #0D1B2A;
    font-weight: 600;
    font-size: 0.92rem;
}
</style>
""", unsafe_allow_html=True)

    st.markdown("""
    <h1>⚖️ LegalEase</h1>
    <p class='page-subtitle'>Upload your legal documents for AI-powered analysis</p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<div class="section-strip">📄 Upload Legal Documents</div>',
                unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Upload one or more Legal PDF Documents",
        type=["pdf"],
        accept_multiple_files=True
    )

    if not uploaded_files:
        return

    st.markdown(
        f'<div class="summary-panel" style="margin-top:0.75rem">'
        f'<div class="summary-row"><span class="summary-key">Files selected</span>'
        f'<span>{len(uploaded_files)}</span></div>'
        + "".join(
            f'<div class="summary-row"><span class="summary-key">📎</span>'
            f'<span class="meta-value">{f.name}</span></div>'
            for f in uploaded_files
        )
        + '</div>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⚡ Analyze Documents", use_container_width=False):

        uploaded_documents = []

        with st.spinner("Analyzing documents…"):

            for uploaded_file in uploaded_files:

                save_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                text = extract_text(save_path)

                if not text.strip():
                    st.warning(f"⚠️ {uploaded_file.name} contains no readable text.")
                    continue

                language      = detect_language(text)
                document_type = detect_document_type(uploaded_file.name, text)
                clauses       = extract_clauses(text)

                document = {
                    "filename":      uploaded_file.name,
                    "text":          text,
                    "language":      language,
                    "document_type": document_type,
                    "clauses":       clauses
                }

                chunks = chunk_document(document)
                create_vector_store(chunks)

                uploaded_documents.append({
                    "filename":      uploaded_file.name,
                    "filepath":      save_path,
                    "text":          text,
                    "language":      language,
                    "document_type": document_type,
                    "clauses":       clauses
                })

        st.session_state.documents = uploaded_documents

        if uploaded_documents:
            first_doc = uploaded_documents[0]
            st.session_state.uploaded_file  = first_doc["filename"]
            st.session_state.file_path      = first_doc["filepath"]
            st.session_state.document_text  = first_doc["text"]
            st.session_state.language       = first_doc["language"]
            st.session_state.document_type  = first_doc["document_type"]
            st.session_state.clauses        = first_doc["clauses"]

        st.session_state.analysis_complete = True
        st.success("✅ All documents processed successfully!")
        st.switch_page("pages/analysis.py")


upload_page()