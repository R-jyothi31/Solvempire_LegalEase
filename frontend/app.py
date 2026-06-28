import streamlit as st

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)

# ----------------------------
# Initialize Session State
# ----------------------------
defaults = {
    "analysis_complete": False,
    "uploaded_file": None,
    "file_path": "",          # Added: set by upload.py
    "document_text": "",
    "language": "",
    "document_type": "",
    "clauses": [],
    "summary": "",
    "rights": "",
    "risks": "",
    "next_steps": "",
    "documents": []           # Added: upload.py stores all docs here
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ----------------------------
# Home Page
# ----------------------------
st.title("⚖️ LegalEase")

st.subheader("AI-Powered Legal Document Assistant")

st.write("""
Welcome to **LegalEase**.

This application helps you:

- 📄 Upload legal documents
- 🌍 Read documents in multiple languages
- 📑 Extract clauses
- ⚖️ Identify legal rights
- ⚠️ Detect risky clauses
- 💡 Generate legal recommendations
""")

st.image(
    "https://img.icons8.com/color/480/artificial-intelligence.png",
    width=200
)

if st.button("🚀 Start Analysis"):
    st.switch_page("pages/upload.py")