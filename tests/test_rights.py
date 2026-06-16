import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)
from agents.rights_law_agent import RightsAgent

agent = RightsAgent()

query = "tenant security deposit"

results = agent.get_relevant_laws(query)

for i, result in enumerate(results):

    print("\n")
    print("=" * 50)

    print(f"Law {i+1}")

    print(result["content"])