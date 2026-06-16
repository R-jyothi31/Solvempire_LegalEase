from llm.gemini_llm import llm

class ExplainerAgent:

    def explain(self, clause):

        prompt = f"""
You are a legal assistant.

Explain the clause in simple English.

Clause:
{clause}

Provide:

1. Meaning
2. Risk
3. User Impact
"""

        response = llm.invoke(prompt)

        return response.content