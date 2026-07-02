import os
from langchain_chroma import Chroma
from rag.embedding import VECTOR_DB_PATH, get_embedding_model

_vectordb = None


def _get_vectordb():
    global _vectordb
    if _vectordb is None:
        _vectordb = Chroma(
            persist_directory=VECTOR_DB_PATH,
            embedding_function=get_embedding_model()
        )
    return _vectordb


def reset_vectordb_cache():
    """Call this after embedding a new document in the same process if
    retrieval seems to be returning stale/missing results — forces the
    next retrieval call to re-open the persisted store from disk."""
    global _vectordb
    _vectordb = None

def retrieve(query, k=5):

    docs = _get_vectordb().similarity_search(

        query=query,

        k=k

    )

    return docs

def retrieve_with_filter(

        query,

        filter_dict,

        k=5

):

    docs = _get_vectordb().similarity_search(

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

    docs = _get_vectordb().get(

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

    docs = _get_vectordb().similarity_search_with_score(

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


def display_results(results):

    for i, doc in enumerate(results):

        print("=" * 70)

        print("Result", i + 1)

        print()

        print(doc.page_content)

        print()

        print(doc.metadata)

        print("=" * 70)

if __name__ == "__main__":

    docs = retrieve(

        "Explain employee rights"

    )

    display_results(docs)
