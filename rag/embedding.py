from langchain_community.vectorstores import Chroma
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def create_vector_store(chunks, metadata):

    db = Chroma.from_texts(
        texts=chunks,
        metadatas=metadata,
        embedding=None,
        persist_directory="vector_store/chromadb"
    )

    db.persist()

    print("Vector Store Created")