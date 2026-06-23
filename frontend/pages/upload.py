import streamlit as st
from utils import save_uploaded_file, analyze_uploaded_document

st.title("Upload Legal Document")
st.write("Upload a legal PDF file")

uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])

if uploaded_file is not None:
    st.success(f"Selected File: {uploaded_file.name}")

    if st.button("Analyze Document"):
        try:
            file_path = save_uploaded_file(uploaded_file)
            result = analyze_uploaded_document(file_path)

            st.session_state["analysis_result"] = result
            st.session_state["uploaded_file_name"] = uploaded_file.name

            st.success("Document analyzed successfully!")

            st.subheader("Document Overview")
            st.write(f"**Document Type:** {result.get('document_type', 'Unknown')}")
            st.write(f"**Total Clauses Processed:** {len(result.get('analysis', []))}")

        except Exception as e:
            st.error(f"Error while analyzing document: {e}")