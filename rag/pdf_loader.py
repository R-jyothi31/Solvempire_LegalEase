import fitz
import os

RAW_DATA_PATH = "data/raw"
TEXT_OUTPUT_PATH = "data/processed/texts"

os.makedirs(TEXT_OUTPUT_PATH, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    text = ""

    doc = fitz.open(pdf_path)

    for page in doc:
        text += page.get_text()

    return text


def process_all_pdfs():

    for root, dirs, files in os.walk(RAW_DATA_PATH):

        for file in files:

            if file.endswith(".pdf"):

                pdf_path = os.path.join(root, file)

                text = extract_text_from_pdf(pdf_path)

                output_file = os.path.join(
                    TEXT_OUTPUT_PATH,
                    file.replace(".pdf", ".txt")
                )

                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(text)

                print(f"Processed {file}")


if __name__ == "__main__":
    process_all_pdfs()