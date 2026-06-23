import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)
from agents.explainer_agent import ExplainerAgent

agent = ExplainerAgent()

clause = """
Tenant shall vacate premises
within 7 days of termination.
"""

result = agent.explain(clause)

print(result)