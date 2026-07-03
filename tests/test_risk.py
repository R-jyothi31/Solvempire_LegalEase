import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.risk_flagging_agent import flag_risks

result = flag_risks(
    "Landlord may terminate immediately without notice."
)

print("=== RISK FLAGGING OUTPUT ===\n")
print(result)