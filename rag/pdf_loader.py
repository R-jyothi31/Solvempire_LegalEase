import fitz
import os

from agents.language_agent import detect_language
from agents.document_parser import detect_document_type
from agents.clause_extractor import extract_clauses


def extract_text(pdf_path):
    """
    Extract text from a PDF.
    """

    text = ""

    doc = fitz.open(pdf_path)

    for page in doc:

        text += page.get_text()

    doc.close()

    return text


def load_document(pdf_path):
    """
    Complete document processing pipeline.
    """

    filename = os.path.basename(pdf_path)

    text = extract_text(pdf_path)

    language = detect_language(text)

    document_type = detect_document_type(
        filename,
        text
    )

    clauses = extract_clauses(text)

    return {

        "filename": filename,

        "text": text,

        "language": language,

        "document_type": document_type,

        "clauses": clauses

    }


def load_multiple_documents(folder_path):
    """
    Process all PDFs inside a folder.
    """

    documents = []

    for file in os.listdir(folder_path):

        if file.endswith(".pdf"):

            pdf_path = os.path.join(
                folder_path,
                file
            )

            documents.append(
                load_document(pdf_path)
            )

    return documents