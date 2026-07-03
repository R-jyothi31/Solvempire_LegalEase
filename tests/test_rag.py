import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rag.pdf_loader import extract_text
from rag.chunker import chunk_document        # Fixed: was split_text_into_chunks
from rag.retriever import retrieve


def test_pdf_loader():
    sample_pdf = os.path.join("data", "raw", "sample.pdf")

    if not os.path.exists(sample_pdf):
        print("Sample PDF not found. Skipping PDF loader test.")
        return

    text = extract_text(sample_pdf)

    assert isinstance(text, str)
    assert len(text) > 0

    print("PDF Loader Test Passed")
    print("Extracted text length:", len(text))


def test_chunker():
    # chunk_document expects the full document dict
    sample_document = {
        "filename": "sample.pdf",
        "text": "This is a sample legal document. " * 50,
        "language": "English",
        "document_type": "Rental Agreement",
        "clauses": [
            "The tenant shall pay rent before the 5th day of every month.",
            "A security deposit of Rs. 20,000 shall be paid.",
            "The landlord may terminate with 30 days notice."
        ]
    }

    chunks = chunk_document(sample_document)

    assert isinstance(chunks, list)
    assert len(chunks) > 0

    print("\nChunker Test Passed")
    print("Number of chunks:", len(chunks))
    print("First chunk preview:", chunks[0].page_content[:200])


def test_retriever():
    query = "What are the consumer rights if a product is defective?"

    try:
        results = retrieve(query)

        assert results is not None
        assert isinstance(results, list)

        print("\nRetriever Test Passed")
        print("Number of retrieved documents:", len(results))

        for i, doc in enumerate(results[:2], start=1):
            print(f"\nResult {i}:")
            print(doc.page_content[:300])

    except Exception as e:
        print("\nRetriever Test Failed")
        print("Error:", e)


if __name__ == "__main__":
    print("Running RAG Tests...\n")

    test_pdf_loader()
    test_chunker()
    test_retriever()

    print("\nAll RAG tests completed.")