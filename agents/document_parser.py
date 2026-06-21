import re


class DocumentParserAgent:
    def __init__(self):
        pass

    def detect_document_type(self, text):
        """
        Detect document type based on keywords found in the uploaded document.
        """
        text_lower = text.lower()

        # -----------------------------
        # 1. Consumer Rights / Consumer Law
        # -----------------------------
        consumer_keywords = [
            "consumer protection",
            "consumer disputes",
            "consumer commission",
            "complaint",
            "defect in goods",
            "deficiency in service",
            "e-commerce",
            "product liability",
            "district commission",
            "state commission",
            "national commission",
            "consumer rights"
        ]

        # -----------------------------
        # 2. Rental Agreement
        # -----------------------------
        rental_keywords = [
            "rent",
            "rental agreement",
            "lease",
            "tenant",
            "landlord",
            "security deposit",
            "premises",
            "monthly rent",
            "lock-in period",
            "vacate"
        ]

        # -----------------------------
        # 3. Employment Agreement
        # -----------------------------
        employment_keywords = [
            "employee",
            "employer",
            "salary",
            "employment",
            "offer letter",
            "internship",
            "nda",
            "non-disclosure",
            "service agreement",
            "probation",
            "termination of employment"
        ]

        # -----------------------------
        # 4. Legal Notice
        # -----------------------------
        legal_notice_keywords = [
            "legal notice",
            "you are hereby called upon",
            "under instructions from my client",
            "notice period",
            "failure to comply",
            "within 15 days",
            "within 30 days",
            "cause of action",
            "demand notice"
        ]

        # -----------------------------
        # 5. Legal Knowledge Documents
        # Acts, Rules, Gazette, etc.
        # -----------------------------
        legal_knowledge_keywords = [
            "act, 2019",
            "rules, 2020",
            "gazette of india",
            "ministry",
            "published by authority",
            "section 3",
            "sub-section",
            "notification",
            "consumer protection act",
            "consumer protection rules",
            "commission rules"
        ]

        # score-based detection
        scores = {
            "Consumer Rights / Consumer Law": 0,
            "Rental Agreement": 0,
            "Employment Agreement": 0,
            "Legal Notice": 0,
            "Legal Knowledge Document": 0
        }

        for word in consumer_keywords:
            if word in text_lower:
                scores["Consumer Rights / Consumer Law"] += 1

        for word in rental_keywords:
            if word in text_lower:
                scores["Rental Agreement"] += 1

        for word in employment_keywords:
            if word in text_lower:
                scores["Employment Agreement"] += 1

        for word in legal_notice_keywords:
            if word in text_lower:
                scores["Legal Notice"] += 1

        for word in legal_knowledge_keywords:
            if word in text_lower:
                scores["Legal Knowledge Document"] += 1

        # pick highest score
        best_type = max(scores, key=scores.get)

        # if nothing matched, fallback
        if scores[best_type] == 0:
            return "General Legal Document"

        return best_type

    def extract_clauses(self, text):
        """
        Extract clauses from uploaded text.
        This tries multiple strategies because different legal PDFs
        have different formatting styles.
        """

        # Clean text first
        text = text.replace("\r", "\n")
        text = re.sub(r"\n{2,}", "\n\n", text).strip()

        clauses = []

        # ---------------------------------------------------
        # Strategy 1: Split by numbered headings like:
        # 1. , 2. , 3.
        # ---------------------------------------------------
        numbered_clauses = re.split(r"\n\s*(\d+\.)", text)

        if len(numbered_clauses) > 3:
            combined = []
            i = 1
            while i < len(numbered_clauses) - 1:
                clause_num = numbered_clauses[i]
                clause_text = numbered_clauses[i + 1].strip()
                combined.append(f"{clause_num} {clause_text}")
                i += 2

            clauses = [c for c in combined if len(c.strip()) > 40]

        # ---------------------------------------------------
        # Strategy 2: Split by "Section", "Clause", etc.
        # ---------------------------------------------------
        if len(clauses) < 2:
            section_split = re.split(
                r"\n\s*(section\s+\d+|clause\s+\d+|article\s+\d+)",
                text,
                flags=re.IGNORECASE
            )

            if len(section_split) > 3:
                combined = []
                i = 1
                while i < len(section_split) - 1:
                    heading = section_split[i]
                    clause_text = section_split[i + 1].strip()
                    combined.append(f"{heading} {clause_text}")
                    i += 2

                clauses = [c for c in combined if len(c.strip()) > 40]

        # ---------------------------------------------------
        # Strategy 3: Split by paragraphs if no structured clauses found
        # ---------------------------------------------------
        if len(clauses) < 2:
            paragraphs = text.split("\n\n")
            clauses = [p.strip() for p in paragraphs if len(p.strip()) > 80]

        # ---------------------------------------------------
        # Final fallback: chunk text manually
        # ---------------------------------------------------
        if len(clauses) == 0:
            chunk_size = 1200
            clauses = [
                text[i:i + chunk_size].strip()
                for i in range(0, len(text), chunk_size)
                if text[i:i + chunk_size].strip()
            ]

        return clauses[:10]