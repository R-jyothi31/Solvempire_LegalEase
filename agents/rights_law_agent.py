class RightsLawAgent:
    def __init__(self):
        pass

    def get_relevant_laws(self, clause, document_type="General Legal Document"):
        if document_type == "Consumer Rights / Consumer Complaint":
            return [{
                "source": "Consumer Protection Act, 2019",
                "law_text": "This section may relate to consumer complaint, refund, compensation, or unfair trade practice."
            }]

        elif document_type == "Rental Agreement":
            return [{
                "source": "Rental Agreement Guidance",
                "law_text": "Check rent amount, deposit, notice period, maintenance duties, and lock-in terms."
            }]

        elif document_type == "Employment Agreement":
            return [{
                "source": "Employment Contract Guidance",
                "law_text": "Check salary, job role, notice period, leave policy, and termination conditions."
            }]

        elif document_type == "Legal Notice":
            return [{
                "source": "Legal Notice Guidance",
                "law_text": "Understand the claim made, deadline for reply, and documents needed to respond."
            }]

        else:
            return [{
                "source": "General Legal Guidance",
                "law_text": "Read this clause carefully and understand your rights, duties, and risks."
            }]