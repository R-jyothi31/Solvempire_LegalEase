from rag.retriever import retrieve
from llm.gemini_llm import llm


def get_rights(clause):
    """
    Retrieve legal rights related to a clause using RAG.
    """

    docs = retrieve(clause, k=4)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are an AI Legal Rights Assistant.

Use ONLY the legal context provided below.

Context:
{context}

Clause:
{clause}

Tasks:

1. Explain the legal rights of the user.
2. Mention legal responsibilities.
3. Mention applicable laws.
4. Mention important legal protections.
5. Give practical advice.

Return in this format:

Rights:
...

Responsibilities:
...

Applicable Laws:
...

Legal Protection:
...

Advice:
...
"""

    try:

        response = llm.invoke(prompt)

        return response.content

    except Exception as e:

        return f"Error: {str(e)}"


def rights_summary(document_text):
    """
    Generate an overall rights summary for the document.
    """

    docs = retrieve(document_text, k=5)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
Summarize the legal rights contained in this document.

Context:
{context}

Document:
{document_text}

Include:

• Main Rights

• Main Responsibilities

• Important Laws

• Consumer Protection

• Recommendations
"""

    try:

        response = llm.invoke(prompt)

        return response.content

    except Exception as e:

        return f"Error: {str(e)}"


def rights_by_clause(clauses):
    """
    Analyze every clause individually.
    """

    results = []

    for i, clause in enumerate(clauses):

        result = get_rights(clause)

        results.append({

            "clause": i + 1,

            "rights": result

        })

    return results