import re

class DocumentParserAgent:

    def detect_document_type(self, text):

        text = text.lower()

        if "tenant" in text or "landlord" in text:
            return "Rental Agreement"

        elif "employee" in text or "employer" in text:
            return "Employment Contract"

        elif "internship" in text:
            return "Internship Agreement"

        elif "confidential" in text:
            return "NDA"

        elif "consumer complaint" in text:
            return "Consumer Complaint"

        elif "legal notice" in text:
            return "Legal Notice"

        return "Unknown"

    def extract_clauses(self, text):

        clauses = re.split(r"\n\d+\.", text)

        cleaned = []

        for clause in clauses:

            clause = clause.strip()

            if clause:
                cleaned.append(clause)

        return cleaned