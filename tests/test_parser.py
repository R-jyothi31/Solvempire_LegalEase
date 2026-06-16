import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from agents.document_parser import DocumentParserAgent

parser = DocumentParserAgent()

sample_text = """
Rental Agreement

1. Tenant shall pay rent before 5th.

2. Landlord may terminate agreement with 30 days notice.

3. Tenant shall maintain property.
"""

doc_type = parser.detect_document_type(sample_text)

clauses = parser.extract_clauses(sample_text)

print("Document Type:")
print(doc_type)

print("\nClauses:")

for i, clause in enumerate(clauses):

    print(f"\nClause {i+1}")
    print(clause)