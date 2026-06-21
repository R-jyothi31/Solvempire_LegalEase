class NextStepsAgent:
    def __init__(self):
        pass

    def suggest_actions(self, document_type, clause, risks):
        if document_type == "Rental Agreement":
            return [
                "Check rent, deposit, notice period, maintenance, and lock-in clause carefully.",
                "Negotiate unclear or unfair clauses before signing.",
                "Keep a signed copy of the agreement and payment proofs."
            ]

        elif document_type == "Employment Agreement":
            return [
                "Check salary, working hours, leave policy, notice period, and termination clause carefully.",
                "Clarify any NDA, bond, or restrictive clauses before signing.",
                "Keep a signed copy of the agreement and offer letter."
            ]

        elif document_type == "Legal Notice":
            return [
                "Read the notice carefully and identify the claim being made.",
                "Collect all related documents, payment proofs, emails, or agreements.",
                "Consult a lawyer or prepare a formal response within the given deadline."
            ]

        elif document_type == "Consumer Rights / Consumer Law":
            return [
                "Check whether the clause explains consumer complaint filing, commission procedure, refund rights, or product/service liability.",
                "Compare the clause with your issue, such as defective product, unfair trade practice, or service deficiency.",
                "Use this information while preparing a consumer complaint or understanding your rights."
            ]

        elif document_type == "Legal Knowledge Document":
            return [
                "This appears to be an official legal reference document such as an Act, Rule, or Gazette notification.",
                "Use it as a legal knowledge source for rights retrieval and explanation.",
                "Do not treat it like a rental or employment agreement."
            ]

        else:
            return [
                "Read the clause carefully and identify the rights and obligations it creates.",
                "Compare it with related laws or supporting documents.",
                "Seek legal guidance if the clause creates financial, legal, or contractual risk."
            ]