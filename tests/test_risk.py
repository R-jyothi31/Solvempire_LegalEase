import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)
from agents.risk_flagging_agent import RiskFlaggingAgent

agent = RiskFlaggingAgent()

print(
    agent.detect_risk(
        "Landlord may terminate immediately without notice."
    )
)