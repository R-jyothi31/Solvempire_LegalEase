from llm.gemini_llm import llm


def explain_clause(clause):
    """
    Explain a legal clause in simple language.
    """

    # Guard against oversized input
    clause = clause[:5000]

    prompt = f"""
You are an AI Legal Assistant.

Explain the following legal clause in very simple English.

Also provide:

1. Simple Explanation
2. Key Points
3. Responsibilities
4. Rights
5. Important Notes

Clause:
{clause}

Return the answer in the following format:

Simple Explanation:
...

Key Points:
- ...

Responsibilities:
- ...

Rights:
- ...

Important Notes:
- ...
"""

    try:
        response = llm.invoke(prompt)
        return response.content

    except Exception as e:
        return f"Error: {str(e)}"


def summarize_document(text):
    """
    Generate a summary of the entire document.
    """

    # Guard against oversized input
    text = text[:12000]

    prompt = f"""
You are a Legal AI Assistant.

Summarize the following legal document.

Include:

1. Document Type
2. Purpose
3. Important Clauses
4. Rights
5. Responsibilities
6. Risks
7. Overall Summary

Document:

{text}
"""

    try:
        response = llm.invoke(prompt)
        return response.content

    except Exception as e:
        return f"Error: {str(e)}"


def explain_multiple_clauses(clauses):
    """
    Explain all clauses one by one.
    """

    explanations = []

    for i, clause in enumerate(clauses):

        explanation = explain_clause(clause)

        explanations.append({
            "clause_number": i + 1,
            "clause": clause,
            "explanation": explanation
        })

    return explanations