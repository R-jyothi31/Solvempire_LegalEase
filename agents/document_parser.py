import re


class DocumentParserAgent:
    def __init__(self):
        pass

    def clean_text(self, text):
        if not text:
            return ""

        # remove extra spaces/newlines
        text = text.replace("\r", " ")
        text = re.sub(r"\n+", "\n", text)
        text = re.sub(r"[ \t]+", " ", text)
        return text.strip()

    def detect_document_type(self, text):
        text = self.clean_text(text).lower()

        # Consumer / complaint related
        consumer_keywords = [
            "consumer", "complaint", "consumer court",
            "deficiency in service", "unfair trade practice",
            "district commission", "state commission",
            "national commission", "refund", "compensation"
        ]

        # Rental related
        rental_keywords = [
            "rent", "tenant", "landlord", "lease",
            "security deposit", "premises", "monthly rent",
            "vacate", "rental agreement"
        ]

        # Employment related
        employment_keywords = [
            "employee", "employer", "salary", "offer letter",
            "employment", "job role", "termination",
            "notice period", "company"
        ]

        # Legal notice related
        notice_keywords = [
            "legal notice", "notice", "demand notice",
            "you are hereby called upon", "failure to comply",
            "under instructions from my client"
        ]

        # score-based detection
        scores = {
            "Consumer Rights / Consumer Complaint": 0,
            "Rental Agreement": 0,
            "Employment Agreement": 0,
            "Legal Notice": 0
        }

        for word in consumer_keywords:
            if word in text:
                scores["Consumer Rights / Consumer Complaint"] += 1

        for word in rental_keywords:
            if word in text:
                scores["Rental Agreement"] += 1

        for word in employment_keywords:
            if word in text:
                scores["Employment Agreement"] += 1

        for word in notice_keywords:
            if word in text:
                scores["Legal Notice"] += 1

        best_type = max(scores, key=scores.get)

        if scores[best_type] == 0:
            return "General Legal Document"

        return best_type

    def extract_clauses(self, text):
        """
        Extract readable clauses/sections from uploaded legal text.
        Works for:
        - numbered clauses
        - headings
        - complaint format paragraphs
        - normal agreement paragraphs
        """
        text = self.clean_text(text)

        if not text:
            return []

        # Split into paragraphs by blank lines or long newlines
        raw_parts = re.split(r"\n\s*\n|\n(?=[A-Z0-9][A-Za-z0-9 ,\-\(\)]{3,50}:?)", text)

        cleaned_parts = []
        for part in raw_parts:
            part = part.strip()

            # remove tiny useless fragments
            if len(part) < 40:
                continue

            # remove too much spacing
            part = re.sub(r"\s+", " ", part)

            cleaned_parts.append(part)

        # If not enough clauses found, fallback by sentence grouping
        if len(cleaned_parts) == 0:
            sentences = re.split(r"(?<=[.!?])\s+", text)
            temp = []
            chunk = ""

            for sentence in sentences:
                if len(chunk) + len(sentence) < 350:
                    chunk += " " + sentence
                else:
                    if len(chunk.strip()) > 40:
                        temp.append(chunk.strip())
                    chunk = sentence

            if len(chunk.strip()) > 40:
                temp.append(chunk.strip())

            cleaned_parts = temp

        # Make clauses short and understandable
        final_clauses = []
        for part in cleaned_parts[:8]:
            short_part = part[:500].strip()
            final_clauses.append(short_part)

        return final_clauses