from rag.retriever import (
    retrieve,
    retrieve_by_file,
    retrieve_by_document_type,
    retrieve_by_language
)

from llm.gemini_llm import llm


def _docs_to_context(docs):
    """Join retrieved doc chunks into a single context string, guarding
    against None / empty page_content."""
    if not docs:
        return ""
    return "\n\n".join(
        doc.page_content for doc in docs if getattr(doc, "page_content", None)
    )


def _retrieve_with_fallback(question, filename=None, document_type=None, language=None):
    attempts = []

    if filename:
        attempts.append(("filename", lambda: retrieve_by_file(question, filename)))
    if document_type:
        attempts.append(("document_type", lambda: retrieve_by_document_type(question, document_type)))
    if language:
        attempts.append(("language", lambda: retrieve_by_language(question, language)))
    # Always keep an unfiltered attempt as the final fallback
    attempts.append(("unfiltered", lambda: retrieve(question)))

    for label, fn in attempts:
        try:
            docs = fn()
        except Exception as e:
            print(f"[rag_chain] Retrieval strategy '{label}' failed: {e}")
            continue

        context = _docs_to_context(docs)
        if context:
            print(f"[rag_chain] Retrieval succeeded via '{label}' strategy "
                  f"({len(docs)} chunk(s)).")
            return context, label

    return "", None


def ask_legal_question(
        question,
        filename=None,
        language=None,
        document_type=None
):
   
    if not question or not question.strip():
        return "Please enter a question."

    context, source = _retrieve_with_fallback(
        question,
        filename=filename,
        document_type=document_type,
        language=language
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

    try:
        response = llm.invoke(prompt)
    except Exception as e:
        print(f"[rag_chain] LLM invocation failed: {e}")
        return (
            "I found relevant information in the document, but the AI model "
            "failed to generate an answer. Please try again in a moment."
        )

    content = getattr(response, "content", None)
    if not content:
        return "The AI model returned an empty response. Please try rephrasing your question."

    return content
