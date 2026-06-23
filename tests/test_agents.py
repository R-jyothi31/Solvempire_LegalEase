import os
import sys

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.document_parser import DocumentParserAgent
from agents.rights_law_agent import RightsLawAgent
from agents.explainer_agent import ExplainerAgent
from agents.risk_flagging_agent import RiskFlaggingAgent
from agents.next_steps_agent import NextStepsAgent


def test_document_parser():
    print("\n--- Testing DocumentParserAgent ---")
    parser = DocumentParserAgent()

    sample_text = """
    This Rental Agreement is made between the landlord and tenant.
    The tenant shall pay rent before the 5th of every month.
    Security deposit of Rs. 20,000 is required.
    """

    doc_type = parser.detect_document_type(sample_text)
    clauses = parser.extract_clauses(sample_text)

    print("Detected Document Type:", doc_type)
    print("Extracted Clauses:", clauses)


def test_rights_law_agent():
    print("\n--- Testing RightsLawAgent ---")
    rights_agent = RightsLawAgent()

    clause = "The tenant must pay a security deposit before moving in."
    laws = rights_agent.get_relevant_laws(clause)

    print("Clause:", clause)
    print("Relevant Laws:", laws)


def test_explainer_agent():
    print("\n--- Testing ExplainerAgent ---")
    explainer = ExplainerAgent()

    clause = "The tenant must pay rent on or before the 5th day of every month."
    explanation = explainer.explain(clause)

    print("Clause:", clause)
    print("Explanation:", explanation)


def test_risk_flagging_agent():
    print("\n--- Testing RiskFlaggingAgent ---")
    risk_agent = RiskFlaggingAgent()

    clause = "The landlord can terminate the agreement at any time without notice."
    risks = risk_agent.detect_risk(clause)

    print("Clause:", clause)
    print("Risks:", risks)


def test_next_steps_agent():
    print("\n--- Testing NextStepsAgent ---")
    next_steps_agent = NextStepsAgent()

    document_type = "Rental Agreement"
    clause = "The landlord can terminate the agreement at any time without notice."
    risks = "This clause may be unfair because it allows termination without notice."

    steps = next_steps_agent.suggest_actions(document_type, clause, risks)

    print("Clause:", clause)
    print("Next Steps:", steps)


if __name__ == "__main__":
    print("Running Agent Tests...")

    test_document_parser()
    test_rights_law_agent()
    test_explainer_agent()
    test_risk_flagging_agent()
    test_next_steps_agent()

    print("\nAll agent tests completed successfully.")