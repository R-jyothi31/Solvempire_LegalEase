from agents.document_parser import DocumentParserAgent
from agents.rights_law_agent import RightsLawAgent
from agents.explainer_agent import ExplainerAgent
from agents.next_steps_agent import NextStepsAgent
from agents.risk_flagging_agent import RiskFlaggingAgent

parser = DocumentParserAgent()

rights = RightsLawAgent()

explainer = ExplainerAgent()

next_steps = NextStepsAgent()

risk_agent = RiskFlaggingAgent()


def analyze_document(text):

    doc_type = parser.detect_document_type(text)

    clauses = parser.extract_clauses(text)

    print("\nDocument Type:")
    print(doc_type)

    for clause in clauses[:3]:

        print("\n")

        print("=" * 60)

        print("Clause:")
        print(clause)

        laws = rights.get_relevant_laws(
            clause
        )

        print("\nRelevant Laws:")
        print(laws)

        explanation = (
            explainer.explain(
                clause
            )
        )

        print("\nExplanation:")
        print(explanation)

        risks = (
            risk_agent.detect_risk(
                clause
            )
        )

        print("\nRisks:")
        print(risks)

        steps = (
            next_steps.suggest_next_steps(
                clause,
                explanation
            )
        )

        print("\nNext Steps:")
        print(steps)