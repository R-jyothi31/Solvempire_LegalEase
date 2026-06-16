class RiskFlaggingAgent:

    risky_words = [

        "terminate immediately",

        "without notice",

        "penalty",

        "forfeit",

        "eviction"

    ]

    def detect_risk(
            self,
            clause
    ):

        clause = clause.lower()

        risks = []

        for word in self.risky_words:

            if word in clause:

                risks.append(word)

        return risks