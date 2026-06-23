import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VECTOR_DB_PATH = os.path.join(BASE_DIR, "vector_store", "chromadb")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectordb = Chroma(
    persist_directory=VECTOR_DB_PATH,
    embedding_function=embedding_model
)


def retrieve(query, k=4, filter_dict=None):
    """
    Retrieve relevant legal chunks from ChromaDB.
    Optional metadata filter can be used later.
    """
    if filter_dict:
        docs = vectordb.similarity_search(
            query=query,
            k=k,
            filter=filter_dict
        )
    else:
        docs = vectordb.similarity_search(
            query=query,
            k=k
        )

    return docs


def retrieve_text(query, k=4, filter_dict=None):
    docs = retrieve(query, k=k, filter_dict=filter_dict)

    return [
        {
            "content": doc.page_content,
            "metadata": doc.metadata
        }
        for doc in docs
    ]