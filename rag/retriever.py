import os

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# -------------------------------------
# Vector Database Path
# -------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

VECTOR_DB_PATH = os.path.join(
    BASE_DIR,
    "vector_store",
    "chromadb"
)


# -------------------------------------
# Multilingual Embedding Model
# -------------------------------------

embedding_model = HuggingFaceEmbeddings(

    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

)


# -------------------------------------
# Load ChromaDB
# -------------------------------------

vectordb = Chroma(

    persist_directory=VECTOR_DB_PATH,

    embedding_function=embedding_model

)


# -------------------------------------
# Basic Retrieval
# -------------------------------------

def retrieve(query, k=5):

    docs = vectordb.similarity_search(

        query=query,

        k=k

    )

    return docs


# -------------------------------------
# Retrieval with Metadata Filter
# -------------------------------------

def retrieve_with_filter(

        query,

        filter_dict,

        k=5

):

    docs = vectordb.similarity_search(

        query=query,

        k=k,

        filter=filter_dict

    )

    return docs


# -------------------------------------
# Retrieve by Document Type
# -------------------------------------

def retrieve_by_document_type(

        query,

        document_type,

        k=5

):

    return retrieve_with_filter(

        query,

        {

            "document_type": document_type

        },

        k

    )


# -------------------------------------
# Retrieve by Language
# -------------------------------------

def retrieve_by_language(

        query,

        language,

        k=5

):

    return retrieve_with_filter(

        query,

        {

            "language": language

        },

        k

    )


# -------------------------------------
# Retrieve by Uploaded File
# -------------------------------------

def retrieve_by_file(

        query,

        filename,

        k=5

):

    return retrieve_with_filter(

        query,

        {

            "source": filename

        },

        k

    )


# -------------------------------------
# Retrieve by Clause Number
# -------------------------------------

def retrieve_clause(

        clause_number,

        filename

):

    docs = vectordb.get(

        where={

            "source": filename,

            "clause_number": clause_number

        }

    )

    return docs


# -------------------------------------
# Retrieve with Similarity Score
# -------------------------------------

def retrieve_scores(

        query,

        k=5

):

    docs = vectordb.similarity_search_with_score(

        query,

        k=k

    )

    return docs


# -------------------------------------
# Convert Docs to Text
# -------------------------------------

def retrieve_text(

        query,

        k=5

):

    docs = retrieve(

        query,

        k

    )

    return [

        {

            "content": doc.page_content,

            "metadata": doc.metadata

        }

        for doc in docs

    ]


# -------------------------------------
# Display Results
# -------------------------------------

def display_results(results):

    for i, doc in enumerate(results):

        print("=" * 70)

        print("Result", i + 1)

        print()

        print(doc.page_content)

        print()

        print(doc.metadata)

        print("=" * 70)


# -------------------------------------
# Testing
# -------------------------------------

if __name__ == "__main__":

    docs = retrieve(

        "Explain employee rights"

    )

    display_results(docs)