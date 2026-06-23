class ExplainerAgent:
    def __init__(self):
        pass

    def explain(self, clause, laws=None):
        clause_lower = clause.lower()

        if "rent" in clause_lower or "deposit" in clause_lower:
            return "This clause talks about rent or deposit. Check the amount, payment date, and refund conditions."

        elif "notice" in clause_lower or "termination" in clause_lower:
            return "This clause explains notice period or ending of the agreement. Check how many days notice must be given."

        elif "consumer" in clause_lower or "complaint" in clause_lower:
            return "This clause is related to consumer rights or complaint filing. It explains how a consumer can raise an issue or seek relief."

        elif "employee" in clause_lower or "salary" in clause_lower or "employer" in clause_lower:
            return "This clause is about employment terms such as salary, duties, or employee responsibilities."

        elif "payment" in clause_lower or "due" in clause_lower:
            return "This clause talks about payment responsibility. Check the amount to be paid and the deadline."

        else:
            short_clause = clause[:180].replace("\n", " ")
            return f"Simple meaning: {short_clause}..."