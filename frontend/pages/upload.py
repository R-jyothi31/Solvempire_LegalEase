import streamlit as st
import os
import sys

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if FRONTEND_DIR not in sys.path:
    sys.path.append(FRONTEND_DIR)

from utils import save_uploaded_file, analyze_uploaded_document

st.title("Upload Legal Document")

uploaded_file = st.file_uploader(
    "Upload a legal PDF file",
    type=["pdf"]
)

if uploaded_file is not None:
    st.write("Selected File:", uploaded_file.name)

    if st.button("Analyze Document"):
        try:
            with st.spinner("Analyzing document..."):
                file_path = save_uploaded_file(uploaded_file)
                result, raw_text = analyze_uploaded_document(file_path)

                st.session_state["uploaded_file_name"] = uploaded_file.name
                st.session_state["analysis_result"] = result
                st.session_state["raw_text"] = raw_text

            st.success("Document analyzed successfully!")
            st.write(f"**Document Type:** {result['document_type']}")
            st.write(f"**Clauses Processed:** {len(result['analysis'])}")
            st.info("Now open Analysis or Clause View from the sidebar.")

        except Exception as e:
            st.error(f"Error while analyzing document: {e}")