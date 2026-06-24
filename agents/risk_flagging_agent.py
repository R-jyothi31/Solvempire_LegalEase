class RiskFlaggingAgent:
    def detect_risk(self, clause):
        clause_lower = clause.lower()
        risks = []

        risk_keywords = {
            "penalty": "This clause may impose a penalty.",
            "terminate": "This clause includes termination-related terms.",
            "evict": "This clause may allow eviction or forced exit.",
            "non-refundable": "This clause may cause loss of money because it is non-refundable.",
            "deduction": "This clause may allow deductions or charges.",
            "confidential": "This clause imposes confidentiality obligations.",
            "bond": "This clause may bind the person for a fixed period.",
            "notice": "This clause contains notice period obligations."
        }

        for keyword, message in risk_keywords.items():
            if keyword in clause_lower:
                risks.append(message)

        if not risks:
            risks.append("No major risk keywords detected, but legal review is still recommended.")

        return risks