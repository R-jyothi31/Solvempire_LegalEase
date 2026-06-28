import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.explainer_agent import explain_clause

clause = """
Tenant shall vacate premises within 7 days of termination.
"""

result = explain_clause(clause)

print("=== EXPLAINER OUTPUT ===\n")
print(result)