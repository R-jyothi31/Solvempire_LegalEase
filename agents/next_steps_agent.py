from llm.gemini_llm import llm

class NextStepsAgent:

    def suggest_next_steps(
            self,
            clause,
            explanation
    ):

        prompt = f"""
Clause:

{clause}

Explanation:

{explanation}

Suggest actionable next steps
for a common person.

Give only bullet points.
"""

        response = llm.invoke(prompt)

        return response.content