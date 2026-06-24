class ExplainerAgent:
    def explain(self, clause):
        clause_clean = " ".join(clause.split())

        short_clause = clause_clean[:220]

        return {
            "summary": short_clause,
            "simple_explanation": (
                "This clause explains an important condition, responsibility, "
                "or rule mentioned in the document."
            )
        }