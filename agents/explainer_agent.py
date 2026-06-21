class ExplainerAgent:
    def __init__(self):
        pass

    def explain(self, clause):
        clause_lower = clause.lower()

        # Rent / Deposit related
        if "rent" in clause_lower or "deposit" in clause_lower:
            return "This clause talks about rent or deposit payment. Check how much you must pay, when to pay, and whether the deposit is refundable."

        # Notice / termination related
        elif "notice" in clause_lower or "terminate" in clause_lower:
            return "This clause explains when the agreement can end and how much notice must be given before leaving or ending the contract."

        # Salary / employment related
        elif "salary" in clause_lower or "employee" in clause_lower or "employer" in clause_lower:
            return "This clause is about job terms such as salary, work duties, or employee responsibilities. Read it carefully before accepting."

        # Complaint / consumer related
        elif "complaint" in clause_lower or "consumer" in clause_lower:
            return "This clause explains consumer rights or complaint process. It helps the user understand how to raise a complaint or seek help."

        # Legal notice related
        elif "legal notice" in clause_lower or "demand" in clause_lower:
            return "This clause is part of a legal notice. It tells what issue is raised and what action is expected from the other person."

        # Default simple explanation
        else:
            short_clause = clause[:180].replace("\n", " ")
            return f"This clause explains an important legal point. In simple words, it means: {short_clause}..."