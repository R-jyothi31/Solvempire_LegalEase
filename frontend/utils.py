import os
import sys

# ---------------------------------------------------
# Path setup
# ---------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))          # frontend/
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))   # Solvempire_LegalEase/

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ---------------------------------------------------
# Imports
# ---------------------------------------------------
from rag.pdf_loader import extract_text_from_pdf
from agents.legal_pipeline import LegalWorkflow
from agents.faq_agent import FAQAgent

UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, "uploaded_docs")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def save_uploaded_file(uploaded_file):
    """
    Save uploaded PDF into uploaded_docs folder.
    """
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


def analyze_uploaded_document(file_path):
    """
    Extract text from uploaded PDF and analyze it using LegalWorkflow.
    """
    try:
        text = extract_text_from_pdf(file_path)

        if not text or not text.strip():
            return {
                "document_type": "Unknown Document",
                "document_summary": "No readable text found in the uploaded PDF.",
                "analysis": [],
                "full_text": ""
            }

        workflow = LegalWorkflow()
        result = workflow.analyze_document(text)

        if not isinstance(result, dict):
            result = {
                "document_type": "Unknown Document",
                "document_summary": "Analysis completed, but output format was invalid.",
                "analysis": []
            }

        result["full_text"] = text
        return result

    except Exception as e:
        return {
            "document_type": "Error",
            "document_summary": f"Error while analyzing document: {str(e)}",
            "analysis": [],
            "full_text": ""
        }


def answer_faq_question(question, analysis_result):
    faq_agent = FAQAgent()
    return faq_agent.answer_question(question, analysis_result)