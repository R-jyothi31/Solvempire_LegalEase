import streamlit as st

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ LegalEase")
st.subheader("AI Legal Document Assistant")

if "analysis_result" not in st.session_state:
    st.session_state["analysis_result"] = None

if "raw_text" not in st.session_state:
    st.session_state["raw_text"] = ""

if "uploaded_file_name" not in st.session_state:
    st.session_state["uploaded_file_name"] = ""

st.markdown("""
### Welcome to LegalEase

Use the sidebar to open:
- Upload
- Analysis
- Clause View
""")