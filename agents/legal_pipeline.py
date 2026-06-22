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

        if not clauses:
            return {
                "document_type": document_type,
                "analysis": [
                    {
                        "clause": "No clear clauses could be extracted from this document.",
                        "laws": [{"source": "System", "law_text": "Try uploading a clearer text-based PDF."}],
                        "explanation": "The uploaded file may be scanned, image-based, or not properly structured for clause extraction.",
                        "risks": "Unable to identify risks because no readable clauses were found.",
                        "next_steps": [
                            "Upload a text-based PDF if possible.",
                            "Check whether the PDF contains selectable text.",
                            "Use OCR if the PDF is image-based."
                        ]
                    }
                ]
            }

        for clause in clauses[:5]:
            laws = self.rights.get_relevant_laws(clause, document_type)
            explanation = self.explainer.explain(clause, laws)
            risks = self.risk.detect_risk(clause)
            next_steps = self.next_steps.suggest_actions(document_type, clause, risks)

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