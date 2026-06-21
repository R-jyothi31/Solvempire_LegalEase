class RightsLawAgent:
    def __init__(self):
        pass

    def get_relevant_laws(self, clause, document_type="General Legal Document"):
        clause_lower = clause.lower()
        matched_laws = []

        # 1) Consumer rights / consumer law documents
        if document_type == "Consumer Rights / Consumer Law":
            matched_laws.append({
                "source": "Consumer Protection Act, 2019",
                "law_text": "This clause may relate to consumer rights, complaint filing, unfair trade practices, defective goods, deficient services, refund rights, or consumer commissions."
            })

            if "e-commerce" in clause_lower:
                matched_laws.append({
                    "source": "Consumer Protection (E-Commerce) Rules",
                    "law_text": "E-commerce entities must provide fair information, grievance redressal, and consumer protection safeguards."
                })

            if "complaint" in clause_lower or "commission" in clause_lower:
                matched_laws.append({
                    "source": "Consumer Disputes Redressal Commission Rules",
                    "law_text": "Consumer commissions handle complaints related to goods, services, compensation, and unfair trade practices."
                })

            return matched_laws

        # 2) Rental agreements
        if document_type == "Rental Agreement":
            matched_laws.append({
                "source": "Rental / Tenancy Guidance",
                "law_text": "Check rent amount, security deposit, notice period, maintenance duties, lock-in clause, and termination conditions carefully."
            })
            return matched_laws

        # 3) Employment agreements
        if document_type == "Employment Agreement":
            matched_laws.append({
                "source": "Employment Contract Guidance",
                "law_text": "Review salary, leave policy, working hours, notice period, confidentiality, and termination clauses carefully."
            })
            return matched_laws

        # 4) Legal notice
        if document_type == "Legal Notice":
            matched_laws.append({
                "source": "Legal Notice Guidance",
                "law_text": "A legal notice should clearly state the issue, demand, timeline, and legal basis for the claim."
            })
            return matched_laws

        # 5) Legal knowledge document / acts / rules / gazette docs
        if document_type == "Legal Knowledge Document":
            matched_laws.append({
                "source": "Legal Reference Document",
                "law_text": "This document appears to be a legal act, rule book, gazette, or official legal reference source used for legal guidance and retrieval."
            })
            return matched_laws

        # 6) Default fallback
        matched_laws.append({
            "source": "General Legal Guidance",
            "law_text": "Review this clause carefully and compare it with the rights and obligations of both parties before signing or responding."
        })

        return matched_laws