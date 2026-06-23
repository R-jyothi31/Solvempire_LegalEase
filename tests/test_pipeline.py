import os
import sys

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.legal_pipeline import LegalWorkflow


def test_pipeline():
    workflow = LegalWorkflow()

    sample_text = """
    CONSUMER COMPLAINT

    I purchased a mobile phone from a seller through an online platform.
    The phone stopped working within 5 days.
    The seller refused refund and replacement.
    The company also denied proper support.
    I want to know my rights and what action I can take.
    """

    result = workflow.analyze_document(sample_text)

    print("\n===== PIPELINE TEST OUTPUT =====")
    print("Document Type:", result.get("document_type", "Unknown"))
    print("Number of Clauses:", len(result.get("analysis", [])))

    for i, item in enumerate(result.get("analysis", []), start=1):
        print(f"\n--- Clause {i} ---")
        print("Clause:", item.get("clause", ""))
        print("Laws:", item.get("laws", ""))
        print("Explanation:", item.get("explanation", ""))
        print("Risks:", item.get("risks", ""))
        print("Next Steps:", item.get("next_steps", ""))


if __name__ == "__main__":
    print("Running Pipeline Test...")
    test_pipeline()
    print("\nPipeline test completed successfully.")