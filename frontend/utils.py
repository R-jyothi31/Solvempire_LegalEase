import os
import sys
import fitz

# --------------------------------------------------
# Add project root folder to Python path
# --------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# Now imports from project folders will work
from agents.legal_pipeline import LegalWorkflow
from agents.faq_agent import FAQAgent

# --------------------------------------------------
# Upload folder
# --------------------------------------------------
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, "data", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --------------------------------------------------
# Create workflow objects
# --------------------------------------------------
workflow = LegalWorkflow()
faq_agent = FAQAgent()


def save_uploaded_file(uploaded_file):
    """
    Save uploaded PDF file into data/uploads folder
    """
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


def extract_text_from_pdf(pdf_path):
    """
    Extract text from PDF using PyMuPDF
    """
    text = ""
    doc = fitz.open(pdf_path)

    for page in doc:
        page_text = page.get_text()
        if page_text:
            text += page_text + "\n"

    return text.strip()


def analyze_uploaded_document(pdf_path):
    """
    Extract text from uploaded PDF and analyze using LegalWorkflow
    """
    text = extract_text_from_pdf(pdf_path)

    if not text.strip():
        return {
            "document_type": "Unknown",
            "analysis": [
                {
                    "clause": "No readable text found in the uploaded PDF.",
                    "laws": [
                        {
                            "source": "System",
                            "law_text": "The uploaded PDF may be image-based or scanned."
                        }
                    ],
                    "explanation": "Please upload a text-based PDF or run OCR on the document first.",
                    "risks": "Unable to analyze because no readable text was extracted.",
                    "next_steps": [
                        "Try uploading a text-based PDF.",
                        "Use OCR if the PDF is scanned.",
                        "Re-upload the document."
                    ]
                }
            ]
        }

    return workflow.analyze_document(text)


def answer_faq_question(question, analysis_result):
    if not analysis_result:
        return "Please upload and analyze a document first."

    if not question or not isinstance(question, str):
        return "Please enter a valid question."

    return faq_agent.answer_question(question, analysis_result)