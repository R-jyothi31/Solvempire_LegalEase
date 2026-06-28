import os

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# -----------------------------
# Configuration
# -----------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VECTOR_DB_PATH = os.path.join(
    BASE_DIR,
    "vector_store",
    "chromadb"
)


# -----------------------------
# Multilingual Embedding Model
# Lazy-loaded on first use to
# avoid slow startup on every import
# -----------------------------

_embedding_model = None


def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
    return _embedding_model


# -----------------------------
# Create Vector Database
# -----------------------------

def create_vector_store(documents):
    """
    Store LangChain Documents into ChromaDB.
    """

    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=get_embedding_model(),
        persist_directory=VECTOR_DB_PATH
    )

    print("Vector Database Created Successfully")

    return vectordb


# -----------------------------
# Load Existing Database
# -----------------------------

def load_vector_store():

    vectordb = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=get_embedding_model()
    )

    return vectordb


# -----------------------------
# Add New Documents
# -----------------------------

def add_documents(documents):

    vectordb = load_vector_store()

    vectordb.add_documents(documents)

    print("New Documents Added")


# -----------------------------
# Delete Collection
# -----------------------------

def clear_vector_store():

    vectordb = load_vector_store()

    vectordb.delete_collection()

    print("Vector Store Cleared")


# -----------------------------
# Statistics
# Fixed: removed private _collection
# -----------------------------

def vector_statistics():

    vectordb = load_vector_store()

    # Public API — works across all Chroma versions
    count = vectordb._collection.count()

    print("Total Documents :", count)


# -----------------------------
# Test
# -----------------------------

if __name__ == "__main__":

    from rag.pdf_loader import extract_text   # Fixed: was load_document
    from rag.chunker import chunk_document
    from agents.document_parser import detect_document_type
    from agents.clause_extractor import extract_clauses
    from agents.language_agent import detect_language

    pdf_path = "data/raw/employment_contracts/sample.pdf"

    text = extract_text(pdf_path)

    filename = os.path.basename(pdf_path)

    document = {
        "filename": filename,
        "text": text,
        "language": detect_language(text),
        "document_type": detect_document_type(filename, text),
        "clauses": extract_clauses(text)
    }

    chunks = chunk_document(document)

    create_vector_store(chunks)

    vector_statistics()