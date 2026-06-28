import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.next_steps_agent import suggest_next_steps

document = {
    "document_type": "Rental Agreement",
    "clauses": [
        "Tenant must vacate property within 7 days.",
        "Short notice period may be unfair to the tenant."
    ]
}

result = suggest_next_steps(document)

print("Next Steps Output:\n")
for step in result:
    print(step)