import os
import sys
import fitz

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from agents.legal_pipeline import LegalWorkflow

UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, "data", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def save_uploaded_file(uploaded_file):
    """
    Save uploaded PDF file
    """
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


def extract_text_from_pdf(pdf_path):
    """
    Extract text from uploaded PDF
    """
    text = ""
    doc = fitz.open(pdf_path)

    for page in doc:
        text += page.get_text()

    doc.close()
    return text


def analyze_uploaded_document(pdf_path):
    """
    Run Legal Workflow on uploaded PDF
    """
    text = extract_text_from_pdf(pdf_path)

    workflow = LegalWorkflow()
    result = workflow.analyze_document(text)

    return result, text