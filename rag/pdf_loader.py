import fitz
import os

def extract_text(pdf_path):

    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    return text

def classify_document(filename):

    filename = filename.lower()

    if "rental" in filename:
        return "rental"

    elif "employment" in filename:
        return "employment"

    elif "notice" in filename:
        return "notice"

    else:
        return "consumer"