import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " "
    ]
)


def chunk_document(document):
    """
    Chunk a processed document while preserving metadata.

    document format:
    {
        "filename": "...",
        "text": "...",
        "language": "...",
        "document_type": "...",
        "clauses": [...]
    }
    """

    documents = []

    clauses = document["clauses"]

    for clause_number, clause in enumerate(clauses, start=1):

        chunks = splitter.split_text(clause)

        for chunk_index, chunk in enumerate(chunks):

            metadata = {

                "source": document["filename"],

                "document_type": document["document_type"],

                "language": document["language"],

                "clause_number": clause_number,

                "chunk_number": chunk_index + 1

            }

            documents.append(

                Document(

                    page_content=chunk,

                    metadata=metadata

                )

            )

    return documents


def chunk_multiple_documents(documents):
    """
    Chunk multiple uploaded documents.
    """

    all_chunks = []

    for document in documents:

        chunks = chunk_document(document)

        all_chunks.extend(chunks)

    return all_chunks


def chunk_statistics(chunks):
    """
    Display chunk statistics.
    """

    print("\n========== Chunk Statistics ==========")

    print(f"Total Chunks : {len(chunks)}")

    if len(chunks) > 0:

        print("\nExample Metadata")

        print(chunks[0].metadata)

        print("\nExample Chunk")

        print(chunks[0].page_content[:300])


if __name__ == "__main__":

    from rag.pdf_loader import load_document

    pdf = load_document(
        "data/raw/employment_contracts/sample.pdf"
    )

    chunks = chunk_document(pdf)

    chunk_statistics(chunks)