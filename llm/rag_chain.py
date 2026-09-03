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


def _friendly_llm_error(e: Exception) -> str:
    """Turn a raw LLM/provider error into a message the user can actually
    act on, instead of a generic 'try again' message that's misleading
    for errors that won't fix themselves by retrying (e.g. a retired
    model, a bad API key)."""
    error_str = str(e)

    if "410" in error_str or "end of life" in error_str.lower() or "no longer available" in error_str.lower():
        return (
            "The AI model configured for this app has been retired by the "
            "provider and is no longer available. This needs to be fixed by "
            "updating the model name in the app's configuration "
            "(llm/gemini_llm.py) — please let the app administrator know."
        )
    if "401" in error_str or "unauthorized" in error_str.lower() or "api key" in error_str.lower():
        return (
            "The AI model's API key appears to be invalid or missing. "
            "Please let the app administrator know."
        )
    if "429" in error_str or "rate limit" in error_str.lower():
        return (
            "The AI model is temporarily rate-limited. Please wait a moment "
            "and try again."
        )
    if "timeout" in error_str.lower():
        return (
            "The AI model took too long to respond. Please try again — if "
            "this keeps happening, try a shorter or simpler question."
        )

    print(f"[rag_chain] Unhandled LLM error: {error_str}")
    return (
        "I found relevant information in the document, but the AI model "
        "failed to generate an answer. Please try again in a moment."
    )


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
        # FIX: previously this always returned the same generic
        # "please try again" message regardless of the actual error,
        # which is misleading for errors like a retired model (410) that
        # won't fix themselves by retrying. Now routed through a
        # specific, actionable message based on what actually failed.
        return _friendly_llm_error(e)

    content = getattr(response, "content", None)
    if not content:
        return "The AI model returned an empty response. Please try rephrasing your question."

    return content
