import os
import sys
import streamlit as st

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
UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "uploads"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

# ----------------------------------------------------
# Upload Page
# ----------------------------------------------------
def upload_page():

    st.title("⚖️ LegalEase")

    st.header("📄 Upload Legal Documents")

    uploaded_files = st.file_uploader(
        "Upload one or more Legal PDF Documents",
        type=["pdf"],
        accept_multiple_files=True
    )

    if not uploaded_files:
        return

    st.success(
        f"{len(uploaded_files)} document(s) selected."
    )

    if st.button("Analyze Documents"):

        uploaded_documents = []

        with st.spinner("Analyzing Documents..."):

            for uploaded_file in uploaded_files:

                save_path = os.path.join(
                    UPLOAD_FOLDER,
                    uploaded_file.name
                )

                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # ---------------------------------
                # Extract Text
                # ---------------------------------
                text = extract_text(save_path)

                if not text.strip():
                    st.warning(
                        f"{uploaded_file.name} contains no readable text."
                    )
                    continue

                # ---------------------------------
                # Detect Language
                # ---------------------------------
                language = detect_language(text)

                # ---------------------------------
                # Detect Document Type
                # ---------------------------------
                document_type = detect_document_type(
                    uploaded_file.name,
                    text
                )

                # ---------------------------------
                # Extract Clauses
                # ---------------------------------
                clauses = extract_clauses(text)

                # ---------------------------------
                # Chunking
                # ---------------------------------
                document = {
                    "filename": uploaded_file.name,
                    "text": text,
                    "language": language,
                    "document_type": document_type,
                    "clauses": clauses
                }

                chunks = chunk_document(document)

                # ---------------------------------
                # Create Embeddings
                # chunk_document() already stores:
                # source, document_type, language,
                # clause_number, chunk_number
                # inside each chunk's metadata —
                # no need to pass metadata separately.
                # ---------------------------------
                create_vector_store(chunks)

                uploaded_documents.append(
                    {
                        "filename": uploaded_file.name,
                        "filepath": save_path,
                        "text": text,
                        "language": language,
                        "document_type": document_type,
                        "clauses": clauses
                    }
                )

        # ---------------------------------
        # Save Session
        # ---------------------------------
        st.session_state.documents = uploaded_documents

        if uploaded_documents:

            first_doc = uploaded_documents[0]

            st.session_state.uploaded_file = first_doc["filename"]
            st.session_state.file_path = first_doc["filepath"]
            st.session_state.document_text = first_doc["text"]
            st.session_state.language = first_doc["language"]
            st.session_state.document_type = first_doc["document_type"]
            st.session_state.clauses = first_doc["clauses"]

        st.session_state.analysis_complete = True

        st.success("All documents processed successfully!")

        st.switch_page("pages/analysis.py")


# ----------------------------------------------------
# IMPORTANT
# ----------------------------------------------------
upload_page()
