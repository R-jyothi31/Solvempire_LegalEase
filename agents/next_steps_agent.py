class NextStepsAgent:
    def suggest_actions(self, document_type, clause, risks):
        doc = document_type.lower()
        clause_lower = clause.lower()

        steps = []

        if "consumer" in doc:
            steps = [
                "Check whether the complaint clearly states the product/service issue.",
                "Collect bills, screenshots, warranty card, and payment proof.",
                "Ask for refund, replacement, or compensation if applicable.",
                "If the seller does not respond, consider filing a consumer complaint."
            ]

        elif "rental" in doc or "lease" in doc or "pg" in doc:
            steps = [
                "Check rent, deposit, notice period, and maintenance terms carefully.",
                "Clarify any lock-in, eviction, or penalty clause before signing.",
                "Keep a signed copy of the agreement and payment proof.",
                "Negotiate any unfair clause before accepting the agreement."
            ]

        elif "employment" in doc or "internship" in doc or "nda" in doc:
            steps = [
                "Check notice period, termination terms, and confidentiality clauses.",
                "Clarify salary, working hours, leave rules, and role expectations.",
                "Keep a signed copy of the agreement for future reference.",
                "Ask the employer to explain any unclear or one-sided term."
            ]

        else:
            steps = [
                "Read the document carefully and identify important obligations.",
                "Check whether any clause creates financial or legal risk.",
                "Keep a copy of the document and supporting proof.",
                "Consult a legal expert if the document creates serious obligations."
            ]

        return steps