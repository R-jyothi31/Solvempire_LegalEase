import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Agents use functions, not classes
from agents.document_parser import detect_document_type, document_summary
from agents.clause_extractor import extract_clauses
from agents.rights_law_agent import get_rights
from agents.explainer_agent import explain_clause
from agents.risk_flagging_agent import flag_risks
from agents.next_steps_agent import suggest_next_steps


def test_document_parser():
    print("\n--- Testing document_parser ---")

    sample_text = """
    This Rental Agreement is made between the landlord and tenant.
    The tenant shall pay rent before the 5th of every month.
    Security deposit of Rs. 20,000 is required.
    """

    doc_type = detect_document_type("rental_agreement.pdf", sample_text)
    clauses = extract_clauses(sample_text)

    print("Detected Document Type:", doc_type)
    print("Number of Clauses:", len(clauses))
    print("First Clause:", clauses[0] if clauses else "None")


def test_rights_law_agent():
    print("\n--- Testing rights_law_agent ---")

    clause = "The tenant must pay a security deposit before moving in."
    result = get_rights(clause)

    print("Clause:", clause)
    print("Rights Output:", result[:300] if result else "None")


def test_explainer_agent():
    print("\n--- Testing explainer_agent ---")

    clause = "The tenant must pay rent on or before the 5th day of every month."
    result = explain_clause(clause)

    print("Clause:", clause)
    print("Explanation:", result[:300] if result else "None")


def test_risk_flagging_agent():
    print("\n--- Testing risk_flagging_agent ---")

    clause = "The landlord can terminate the agreement at any time without notice."
    result = flag_risks(clause)

    print("Clause:", clause)
    print("Risks:", result[:300] if result else "None")


def test_next_steps_agent():
    print("\n--- Testing next_steps_agent ---")

    document = {
        "document_type": "Rental Agreement",
        "clauses": [
            "The landlord can terminate the agreement at any time without notice."
        ]
    }

    result = suggest_next_steps(document)

    print("Next Steps:")
    for step in result[:5]:
        print("-", step)


if __name__ == "__main__":
    print("Running Agent Tests...")

    test_document_parser()
    test_rights_law_agent()
    test_explainer_agent()
    test_risk_flagging_agent()
    test_next_steps_agent()

    print("\nAll agent tests completed.")