from rag.retriever import (
    retrieve,
    retrieve_by_file,
    retrieve_by_document_type,
    retrieve_by_language
)

from llm.gemini_llm import llm


def ask_legal_question(
        question,
        filename=None,
        language=None,
        document_type=None
):
    """
    Main RAG pipeline.
    """

    if filename:
        docs = retrieve_by_file(
            question,
            filename
        )

    elif document_type:
        docs = retrieve_by_document_type(
            question,
            document_type
        )

    elif language:
        docs = retrieve_by_language(
            question,
            language
        )

    else:
        docs = retrieve(
            question
        )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    if not context:
        return "No relevant information found in the uploaded documents."

    prompt = f"""
You are LegalEase, an AI-powered Legal Document Assistant.

Use ONLY the legal information provided below.

=========================
Legal Context
=========================

{context}

=========================
User Question
=========================

{question}

=========================
Instructions
=========================

1. Answer only from the provided legal context.
2. If the answer is unavailable, say:
   "I couldn't find this information in the uploaded documents."
3. Explain in simple language.
4. Mention applicable legal rights.
5. Mention legal risks if any.
6. Suggest the next legal steps.
7. If applicable, mention the relevant law.

Provide the answer in a clear, structured format.
"""

    response = llm.invoke(prompt)

    return response.content