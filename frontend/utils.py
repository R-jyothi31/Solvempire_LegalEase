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

# --------------------------------------------------
# Correct imports — agents use functions, not classes
# --------------------------------------------------
from agents.clause_extractor import extract_clauses
from agents.document_parser import detect_document_type
from agents.explainer_agent import explain_clause
from agents.risk_flagging_agent import flag_risks
from agents.rights_law_agent import get_rights
from agents.next_steps_agent import suggest_next_steps
from agents.faq_agent import FAQAgent

# --------------------------------------------------
# Upload folder
# --------------------------------------------------
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, "data", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

faq_agent = FAQAgent()


def save_uploaded_file(uploaded_file):
    """
    Save uploaded PDF file into data/uploads folder.
    """
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


def extract_text_from_pdf(pdf_path):
    """
    Extract text from PDF using PyMuPDF.
    """
    text = ""
    doc = fitz.open(pdf_path)

    for page in doc:
        page_text = page.get_text()
        if page_text:
            text += page_text + "\n"

    doc.close()
    return text.strip()


def analyze_uploaded_document(pdf_path):
    """
    Extract text from uploaded PDF and run full analysis pipeline.
    """
    text = extract_text_from_pdf(pdf_path)

    if not text.strip():
        return {
            "document_type": "Unknown",
            "analysis": [
                {
                    "clause": "No readable text found in the uploaded PDF.",
                    "laws": "The uploaded PDF may be image-based or scanned.",
                    "explanation": "Please upload a text-based PDF or run OCR first.",
                    "risks": "Unable to analyze — no readable text extracted.",
                    "next_steps": [
                        "Try uploading a text-based PDF.",
                        "Use OCR if the PDF is scanned.",
                        "Re-upload the document."
                    ]
                }
            ]
        }

    # Detect document type
    from agents.language_agent import detect_language
    filename = os.path.basename(pdf_path)
    document_type = detect_document_type(filename, text)
    language = detect_language(text)

    # Extract clauses
    clauses = extract_clauses(text)

    # Analyze each clause
    analysis = []
    for clause in clauses:
        analysis.append({
            "clause": clause,
            "explanation": explain_clause(clause),
            "risks": flag_risks(clause),
            "laws": get_rights(clause),
            "next_steps": []
        })

    return {
        "document_type": document_type,
        "language": language,
        "analysis": analysis
    }


def answer_faq_question(question, analysis_result):
    if not analysis_result:
        return "Please upload and analyze a document first."

    if not question or not isinstance(question, str):
        return "Please enter a valid question."

    return faq_agent.answer_question(question, analysis_result)