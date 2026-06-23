class NextStepsAgent:
    def __init__(self):
        pass

    def suggest_actions(self, document_type, clause, risks):
        if document_type == "Consumer Rights / Consumer Complaint":
            return [
                "Check the issue mentioned in the complaint.",
                "Collect bills, receipts, and proof related to the problem.",
                "See whether refund, replacement, or compensation is being requested."
            ]

        elif document_type == "Rental Agreement":
            return [
                "Check rent, deposit, and notice period.",
                "Ask about unclear clauses before signing.",
                "Keep a signed copy of the agreement."
            ]

        elif document_type == "Employment Agreement":
            return [
                "Check salary, notice period, and job role.",
                "Read termination and leave rules carefully.",
                "Keep a signed copy of the contract."
            ]

        elif document_type == "Legal Notice":
            return [
                "Read the notice carefully.",
                "Collect documents related to the issue.",
                "Respond within the deadline if required."
            ]

        else:
            return [
                "Read the clause carefully.",
                "Check if it creates any legal duty or risk.",
                "Take legal advice if the document is important."
            ]