import os

from langchain_community.vectorstores import Chroma

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)

from langchain_core.documents import Document

CHUNK_FOLDER = "data/processed/chunks"

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

documents = []

for file in os.listdir(CHUNK_FOLDER):

    if file.endswith(".txt"):

        with open(
            os.path.join(CHUNK_FOLDER, file),
            "r",
            encoding="utf-8"
        ) as f:

            text = f.read()

        documents.append(
            Document(
                page_content=text,
                metadata={"source": file}
            )
        )

vectordb = Chroma.from_documents(
    documents=documents,
    embedding=embedding_model,
    persist_directory="vector_store/chroma_db"
)

print("Vector Database Created")