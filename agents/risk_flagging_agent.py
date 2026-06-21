class RiskFlaggingAgent:
    def __init__(self):
        pass

    def detect_risk(self, clause, document_type="General Legal Document"):
        clause_lower = clause.lower()
        risks = []

        if document_type == "Consumer Rights / Consumer Law":
            # Consumer law gazette documents are usually procedural, not contract-risk documents
            if "penalty" in clause_lower:
                risks.append("This clause mentions a penalty or legal consequence.")
            if "appeal" in clause_lower or "अपील" in clause_lower:
                risks.append("This clause may affect appeal rights, procedure, or limitation period.")
            if not risks:
                risks.append("This appears to be an informational/procedural consumer law clause, not a risky private contract clause.")
            return risks

        # Rental / employment / notice risk detection
        if "non-refundable" in clause_lower:
            risks.append("This clause may cause financial loss because the amount is non-refundable.")
        if "terminate without notice" in clause_lower:
            risks.append("This clause allows termination without notice.")
        if "penalty" in clause_lower:
            risks.append("This clause contains penalty terms.")
        if "deduct" in clause_lower or "deduction" in clause_lower:
            risks.append("This clause allows deductions.")
        if "confidentiality" in clause_lower:
            risks.append("This clause imposes confidentiality obligations.")
        if "eviction" in clause_lower:
            risks.append("This clause may affect possession or eviction rights.")

        if not risks:
            risks.append("No major risk keywords detected, but review is still recommended.")

        return risks