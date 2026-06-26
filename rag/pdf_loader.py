import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path):
    """
    Extract full text from a PDF file and return it as a string.
    """
    text = ""

    try:
        doc = fitz.open(pdf_path)

        for page in doc:
            page_text = page.get_text("text")
            if page_text:
                text += page_text + "\n"

        doc.close()
        return text.strip()

    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")