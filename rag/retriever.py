from langchain_community.vectorstores import Chroma
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="vector_store/chromadb"
)

def classify_query(query):

    query = query.lower()

    if any(word in query for word in
           ["tenant", "lease", "rent"]):
        return "rental"

    elif any(word in query for word in
             ["salary", "employee", "probation"]):
        return "employment"

    elif any(word in query for word in
             ["notice", "legal notice"]):
        return "notice"

    else:
        return "consumer"


def retrieve(query):

    category = classify_query(query)

    docs = db.similarity_search(
        query,
        k=5,
        filter={
            "category": category
        }
    )

    return docs