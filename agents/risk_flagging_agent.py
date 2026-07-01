from rag.retriever import retrieve
from llm.gemini_llm import llm


def flag_risks(clause):
    """
    Identify risks in a legal clause using RAG.
    """

    docs = retrieve(clause, k=4)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are an AI Legal Risk Analyst.

Use ONLY the legal context provided below.

Context:
{context}

Clause:
{clause}

Tasks:

1. Identify any risky or unfair terms.
2. Highlight one-sided obligations.
3. Flag vague or ambiguous language.
4. Mention penalty or liability risks.
5. Give a risk level: Low / Medium / High.

Return in this format:

Risk Level:
...

Risky Terms:
- ...

One-Sided Obligations:
- ...

Vague Language:
- ...

Penalty / Liability Risks:
- ...

Recommendation:
...
"""

    try:
        response = llm.invoke(prompt)
        return response.content

    except Exception as e:
        return f"Error: {str(e)}"


def flag_all_clauses(clauses):
    """
    Flag risks across all clauses.
    """

    results = []

    for i, clause in enumerate(clauses):

        result = flag_risks(clause)

        results.append({
            "clause_number": i + 1,
            "clause": clause,
            "risks": result
        })

    return results


def overall_risk_summary(clauses):
    """
    Generate a high-level risk summary for the entire document.
    """

    combined = "\n\n".join(clauses)

    docs = retrieve(combined, k=5)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are an AI Legal Risk Analyst.

Analyze the following legal document and provide an overall risk assessment.

Context:
{context}

Document Clauses:
{combined}

Include:

- Overall Risk Level (Low / Medium / High)
- Top 3 Risky Clauses
- Major Red Flags
- Recommendations
"""

    try:
        response = llm.invoke(prompt)
        return response.content

    except Exception as e:
        return f"Error: {str(e)}"