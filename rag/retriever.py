from langchain_community.vectorstores import Chroma

from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectordb = Chroma(
    persist_directory="vector_store/chroma_db",
    embedding_function=embedding_model
)

retriever = vectordb.as_retriever(
    search_kwargs={"k": 3}
)


def retrieve(query):

    docs = retriever.invoke(query)

    return docs