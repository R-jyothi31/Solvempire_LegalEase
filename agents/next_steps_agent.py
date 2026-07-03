from rag.retriever import retrieve
from llm.gemini_llm import llm


def suggest_next_steps(document):
    """
    Generate practical legal recommendations for the uploaded document.

    document = {
        "filename": "...",
        "document_type": "...",
        "language": "...",
        "clauses": [...]
    }
    """
    if isinstance(document, dict):

        document_type = document.get("document_type", "Unknown")
        clauses = document.get("clauses", [])

        if clauses:
            context = "\n\n".join(clauses)
        else:
            context = document.get("document_text", "")

    else:
        document_type = "Unknown"
        context = str(document)

    docs = retrieve(context, k=5)

    legal_context = "\n\n".join(
        doc.page_content for doc in docs
    )



    prompt = f"""
You are an AI Legal Advisor.

Document Type:
{document_type}

Document Clauses:
{context}

Legal Context:
{legal_context}

Based on the document,

Provide:

1. Overall Summary

2. Recommended Next Steps

3. Documents Required

4. Precautions

5. Legal Advice

6. Government Authority (if applicable)

7. Whether Lawyer Consultation is Recommended

Return your answer in bullet points.
"""

    try:

        response = llm.invoke(prompt)

        answer = response.content

        recommendations = []

        for line in answer.split("\n"):

            if line.strip():

                recommendations.append(line.strip())

        return recommendations

    except Exception as e:

        return [
            f"Error: {str(e)}"
        ]


def generate_checklist(document):
    """
    Create a checklist for the uploaded document.
    """

    document_type = document.get("document_type", "")

    checklist = [

        "Read every clause carefully.",

        "Verify names and dates.",

        "Check payment terms.",

        "Understand your legal rights.",

        "Save a signed copy."
    ]

    if document_type == "Rental Agreement":

        checklist.extend([

            "Verify security deposit.",

            "Confirm notice period.",

            "Inspect property before signing."

        ])

    elif document_type == "Employment Contract":

        checklist.extend([

            "Check salary details.",

            "Verify leave policy.",

            "Read termination clause."

        ])

    elif document_type == "Legal Notice":

        checklist.extend([

            "Read allegations carefully.",

            "Collect supporting evidence.",

            "Respond within the prescribed time."

        ])

    elif document_type == "Consumer Complaint":

        checklist.extend([

            "Keep purchase receipts.",

            "Maintain communication records.",

            "Prepare supporting documents."

        ])

    return checklist


def emergency_actions(document_type):
    """
    Show urgent actions for high-risk documents.
    """

    actions = {

        "Rental Agreement": [
            "Verify landlord ownership.",
            "Do not pay cash without receipt.",
            "Check eviction clause."
        ],

        "Employment Contract": [
            "Review salary clause.",
            "Check probation period.",
            "Review termination policy."
        ],

        "Legal Notice": [
            "Do not ignore the notice.",
            "Reply within the deadline.",
            "Consult a lawyer if necessary."
        ],

        "Consumer Complaint": [
            "Collect invoices.",
            "Keep warranty documents.",
            "Contact consumer forum if required."
        ]
    }

    return actions.get(
        document_type,
        [
            "Read the document carefully.",
            "Consult a legal expert if required."
        ]
    )