import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.document_parser import detect_document_type
from agents.clause_extractor import extract_clauses

sample_text = """
Rental Agreement

1. Tenant shall pay rent before 5th.

2. Landlord may terminate agreement with 30 days notice.

3. Tenant shall maintain property.
"""

doc_type = detect_document_type("rental_agreement.pdf", sample_text)
clauses = extract_clauses(sample_text)

print("Document Type:")
print(doc_type)

print("\nClauses:")
for i, clause in enumerate(clauses, start=1):
    print(f"\nClause {i}")
    print(clause)