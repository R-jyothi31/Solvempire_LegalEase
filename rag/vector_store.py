import os

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Language detection
from multilingual.language_detector import detect_language

CHUNK_FOLDER = "data/processed/chunks"

# Multilingual embedding model (supports 50+ languages)
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

documents = []


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


for file in os.listdir(CHUNK_FOLDER):

    if file.endswith(".txt"):

        file_path = os.path.join(CHUNK_FOLDER, file)

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            text = f.read()

        # Detect language of this chunk
        language = detect_language(text)

        # Detect document type from filename
        document_type = classify_document(file)

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": file,
                    "language": language,
                    "document_type": document_type
                }
            )
        )

vectordb = Chroma.from_documents(
    documents=documents,
    embedding=embedding_model,
    persist_directory="vector_store/chroma_db"
)

vectordb.persist()

print("✅ Multilingual Vector Database Created Successfully")