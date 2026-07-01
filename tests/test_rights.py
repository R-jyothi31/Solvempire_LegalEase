import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.rights_law_agent import get_rights

sample_clause = """
The seller refused to replace the defective product
even though it was under warranty.
"""

result = get_rights(sample_clause)

print("=== RIGHTS AGENT OUTPUT ===\n")
print(result)