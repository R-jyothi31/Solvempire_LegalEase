import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)
from agents.next_steps_agent import NextStepsAgent

agent = NextStepsAgent()

result = agent.suggest_next_steps(
    "Tenant must vacate property",
    "Tenant has 7 days to leave"
)

print(result)