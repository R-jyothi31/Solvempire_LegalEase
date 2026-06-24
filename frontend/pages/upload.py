import streamlit as st
from utils import save_uploaded_file, analyze_uploaded_document

st.title("Upload Legal Document")
st.write("Upload a legal PDF file")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])


def analyze_and_store(uploaded_file):
    """
    Save uploaded file, analyze it, and store result in session.
    """
    file_path = save_uploaded_file(uploaded_file)
    result = analyze_uploaded_document(file_path)

    st.session_state["uploaded_file_path"] = file_path
    st.session_state["analysis_result"] = result
    return result


if uploaded_file is not None:
    st.success(f"Selected File: {uploaded_file.name}")

    col1, col2, col3 = st.columns(3)

    # -------------------------------------------------
    # Analyze Document -> analyze + open Analysis page
    # -------------------------------------------------
    with col1:
        if st.button("Analyze Document", use_container_width=True):
            with st.spinner("Analyzing document..."):
                try:
                    analyze_and_store(uploaded_file)

                    # tell app.py which page to open
                    st.session_state["current_page"] = "analysis"

                    # rerun app so app.py loads analysis page
                    st.rerun()

                except Exception as e:
                    st.error(f"Error while analyzing document: {str(e)}")

    # -------------------------------------------------
    # Clause View -> analyze if needed + open Clause page
    # -------------------------------------------------
    with col2:
        if st.button("Clause View", use_container_width=True):
            with st.spinner("Opening clause view..."):
                try:
                    # if not analyzed yet, analyze first
                    if st.session_state.get("analysis_result") is None:
                        analyze_and_store(uploaded_file)

                    st.session_state["current_page"] = "clause"
                    st.rerun()

                except Exception as e:
                    st.error(f"Error while opening Clause View: {str(e)}")

    # -------------------------------------------------
    # FAQ -> analyze if needed + open FAQ page
    # -------------------------------------------------
    with col3:
        if st.button("FAQ", use_container_width=True):
            with st.spinner("Opening FAQ..."):
                try:
                    # if not analyzed yet, analyze first
                    if st.session_state.get("analysis_result") is None:
                        analyze_and_store(uploaded_file)

                    st.session_state["current_page"] = "faq"
                    st.rerun()

                except Exception as e:
                    st.error(f"Error while opening FAQ: {str(e)}")