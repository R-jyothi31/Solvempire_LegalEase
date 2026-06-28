import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.clause_extractor import extract_clauses
from agents.document_parser import detect_document_type
from agents.explainer_agent import explain_clause
from agents.risk_flagging_agent import flag_risks
from agents.rights_law_agent import get_rights


def test_pipeline():
    sample_text = """
    CONSUMER COMPLAINT

    I purchased a mobile phone from a seller through an online platform.
    The phone stopped working within 5 days.
    The seller refused refund and replacement.
    The company also denied proper support.
    I want to know my rights and what action I can take.
    """

    document_type = detect_document_type("consumer_complaint.pdf", sample_text)
    clauses = extract_clauses(sample_text)

    print("\n===== PIPELINE TEST OUTPUT =====")
    print("Document Type:", document_type)
    print("Number of Clauses:", len(clauses))

    for i, clause in enumerate(clauses, start=1):
        print(f"\n--- Clause {i} ---")
        print("Clause:", clause[:200])
        print("Explanation:", explain_clause(clause)[:200])
        print("Risks:", flag_risks(clause)[:200])
        print("Laws:", get_rights(clause)[:200])


if __name__ == "__main__":
    print("Running Pipeline Test...")
    test_pipeline()
    print("\nPipeline test completed.")