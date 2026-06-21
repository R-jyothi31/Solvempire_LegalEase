from agents.document_parser import DocumentParserAgent
from agents.rights_law_agent import RightsLawAgent
from agents.explainer_agent import ExplainerAgent
from agents.risk_flagging_agent import RiskFlaggingAgent
from agents.next_steps_agent import NextStepsAgent


class LegalWorkflow:
    def __init__(self):
        self.parser = DocumentParserAgent()
        self.rights = RightsLawAgent()
        self.explainer = ExplainerAgent()
        self.risk = RiskFlaggingAgent()
        self.next_steps = NextStepsAgent()

    def analyze_document(self, text):
        # Step 1: detect type
        document_type = self.parser.detect_document_type(text)

        # Step 2: extract better clauses
        clauses = self.parser.extract_clauses(text)

        if not clauses:
            clauses = [text[:1500]]

        results = []

        for clause in clauses[:5]:
            laws = self.rights.get_relevant_laws(clause, document_type)
            explanation = self.explainer.explain(clause, document_type)
            risks = self.risk.detect_risk(clause, document_type)
            next_steps = self.next_steps.suggest_actions(
                document_type,
                clause,
                risks
            )

            results.append({
                "clause": clause,
                "laws": laws,
                "explanation": explanation,
                "risks": risks,
                "next_steps": next_steps
            })

        return {
            "document_type": document_type,
            "analysis": results
        }