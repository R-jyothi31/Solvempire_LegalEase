import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)
from agents.legal_pipeline import analyze_document

text = """
Rental Agreement

1. Tenant shall pay rent before 5th.

2. Landlord may terminate immediately without notice.

3. Tenant shall vacate property after termination.
"""

analyze_document(text)