import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.rights_law_agent import RightsLawAgent

agent = RightsLawAgent()

sample_clause = """
The seller refused to replace the defective product even though it was under warranty.
"""

result = agent.get_relevant_laws(sample_clause)

print("=== RIGHTS AGENT OUTPUT ===\n")

# If result is a dictionary
if isinstance(result, dict):
    for key, value in result.items():
        print(f"{key}: {value}")

# If result is a list
elif isinstance(result, list):
    for i, item in enumerate(result, start=1):
        print(f"\nResult {i}:")
        print(item)

# If result is a string
else:
    print(result)