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
        document_type = self.parser.detect_document_type(text)
        clauses = self.parser.extract_clauses(text)

        results = []

        for clause in clauses[:8]:
            laws = self.rights.get_relevant_laws(clause)

            explanation_output = self.explainer.explain(clause)

            if isinstance(explanation_output, dict):
                summary = explanation_output.get("summary", "")
                explanation = explanation_output.get("simple_explanation", "")
            else:
                summary = str(explanation_output)
                explanation = str(explanation_output)

            risks = self.risk.detect_risk(clause)
            next_steps = self.next_steps.suggest_actions(
                document_type,
                clause,
                risks
            )

            results.append({
                "clause": clause,
                "summary": summary,
                "explanation": explanation,
                "laws": laws if isinstance(laws, list) else [str(laws)],
                "risks": risks if isinstance(risks, list) else [str(risks)],
                "next_steps": next_steps if isinstance(next_steps, list) else [str(next_steps)]
            })

        document_summary = self._build_document_summary(document_type, results)

        return {
            "document_type": document_type,
            "document_summary": document_summary,
            "analysis": results
        }

    def _build_document_summary(self, document_type, results):
        if not results:
            return f"The uploaded file appears to be a {document_type}, but no clear clauses were extracted."

        points = []
        for item in results[:5]:
            if item.get("summary"):
                points.append(item["summary"])

        if not points:
            return f"This document is identified as {document_type}. Clause extraction was limited."

        summary_text = "\n".join([f"- {p}" for p in points[:5]])
        return f"This document is identified as {document_type}. Main extracted points are:\n{summary_text}"