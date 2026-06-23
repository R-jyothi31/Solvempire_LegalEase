import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.next_steps_agent import NextStepsAgent

agent = NextStepsAgent()

result = agent.suggest_actions(
    "Rental Agreement",
    "Tenant must vacate property within 7 days.",
    "Short notice period may be unfair to the tenant."
)

print("Next Steps Output:\n")
print(result)