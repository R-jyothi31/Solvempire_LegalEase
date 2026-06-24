import re


class FAQAgent:
    def __init__(self):
        pass

    def answer_question(self, question, analysis_result):
        """
        analysis_result expected format:
        {
            "document_type": "...",
            "document_summary": "...",
            "analysis": [
                {
                    "clause": "...",
                    "summary": "...",
                    "explanation": "...",
                    "laws": [...],
                    "risks": [...],
                    "next_steps": [...]
                }
            ]
        }
        """

        if not analysis_result or not isinstance(analysis_result, dict):
            return "No analyzed document found. Please upload and analyze a document first."

        question_lower = question.lower().strip()

        document_type = analysis_result.get("document_type", "Unknown Document")
        document_summary = analysis_result.get("document_summary", "")
        clauses = analysis_result.get("analysis", [])

        # ---------------------------
        # 1) DOCUMENT TYPE QUESTIONS
        # ---------------------------
        if self._contains_any(question_lower, [
            "what type of document",
            "document type",
            "which document",
            "what document is this"
        ]):
            return f"This document is identified as: {document_type}"

        # ---------------------------
        # 2) SUMMARY QUESTIONS
        # ---------------------------
        if self._contains_any(question_lower, [
            "summarize",
            "summary",
            "main points",
            "key points",
            "overview",
            "what is this document about"
        ]):
            return self._answer_summary(document_type, document_summary, clauses)

        # ---------------------------
        # 3) MAIN CLAUSES QUESTIONS
        # ---------------------------
        if self._contains_any(question_lower, [
            "main clauses",
            "important clauses",
            "important points",
            "clauses in this document",
            "what are the clauses"
        ]):
            return self._answer_main_clauses(clauses)

        # ---------------------------
        # 4) RISK QUESTIONS
        # ---------------------------
        if self._contains_any(question_lower, [
            "risk",
            "risky",
            "danger",
            "unsafe clause",
            "problematic clause",
            "unfair clause"
        ]):
            return self._answer_risks(clauses)

        # ---------------------------
        # 5) RIGHTS / LAW QUESTIONS
        # ---------------------------
        if self._contains_any(question_lower, [
            "rights",
            "relevant law",
            "law",
            "legal protection",
            "which law applies",
            "consumer right"
        ]):
            return self._answer_rights_laws(clauses)

        # ---------------------------
        # 6) NEXT STEP QUESTIONS
        # ---------------------------
        if self._contains_any(question_lower, [
            "next step",
            "what should i do next",
            "what to do next",
            "what action",
            "what should the user do",
            "what should i do"
        ]):
            return self._answer_next_steps(clauses)

        # ---------------------------
        # 7) RENT / DEPOSIT / NOTICE / LOCK-IN
        # ---------------------------
        if self._contains_any(question_lower, [
            "rent",
            "deposit",
            "security deposit",
            "notice period",
            "lock-in",
            "maintenance",
            "eviction"
        ]):
            return self._search_clause_by_keywords(
                clauses,
                ["rent", "deposit", "security deposit", "notice", "lock-in", "maintenance", "eviction"],
                "I could not find a clear rent/deposit/notice-related clause in this document."
            )

        # ---------------------------
        # 8) EMPLOYMENT QUESTIONS
        # ---------------------------
        if self._contains_any(question_lower, [
            "salary",
            "termination",
            "confidentiality",
            "nda",
            "notice period",
            "employee responsibility",
            "working hours",
            "leave",
            "bond"
        ]):
            return self._search_clause_by_keywords(
                clauses,
                ["salary", "termination", "confidential", "nda", "notice", "employee", "working hours", "leave", "bond"],
                "I could not find a clear employment-related clause in this document."
            )

        # ---------------------------
        # 9) CONSUMER QUESTIONS
        # ---------------------------
        if self._contains_any(question_lower, [
            "refund",
            "replacement",
            "compensation",
            "defective product",
            "service deficiency",
            "seller",
            "consumer complaint"
        ]):
            return self._search_clause_by_keywords(
                clauses,
                ["refund", "replacement", "compensation", "defective", "service", "seller", "consumer"],
                "I could not find a clear consumer complaint-related clause in this document."
            )

        # ---------------------------
        # 10) FALLBACK SMART SEARCH
        # ---------------------------
        fallback = self._smart_keyword_search(question_lower, clauses)
        if fallback:
            return fallback

        # ---------------------------
        # 11) FINAL FALLBACK
        # ---------------------------
        return self._answer_summary(document_type, document_summary, clauses)

    # ==========================================================
    # Helper functions
    # ==========================================================

    def _contains_any(self, text, keywords):
        return any(k in text for k in keywords)

    def _answer_summary(self, document_type, document_summary, clauses):
        if document_summary:
            return f"Document Type: {document_type}\n\nSummary:\n{document_summary}"

        if not clauses:
            return f"This document is identified as: {document_type}. No clause summary was extracted."

        top_points = []
        for i, item in enumerate(clauses[:5], start=1):
            summary = item.get("summary") or item.get("explanation") or item.get("clause", "")
            if summary:
                top_points.append(f"{i}. {summary}")

        if top_points:
            return f"Document Type: {document_type}\n\nMain points from the document:\n" + "\n".join(top_points)

        return f"This document is identified as: {document_type}, but no summary content was extracted."

    def _answer_main_clauses(self, clauses):
        if not clauses:
            return "No clauses were extracted from the document."

        lines = []
        for i, item in enumerate(clauses[:8], start=1):
            clause_text = item.get("clause", "").strip()
            summary = item.get("summary", "").strip()

            if summary:
                lines.append(f"{i}. {summary}")
            elif clause_text:
                lines.append(f"{i}. {clause_text[:250]}")

        if not lines:
            return "No clear clauses were found in the document."

        return "Important clauses / points found in the document:\n\n" + "\n".join(lines)

    def _answer_risks(self, clauses):
        if not clauses:
            return "No clauses available to check for risks."

        risk_lines = []
        for i, item in enumerate(clauses, start=1):
            risks = item.get("risks", [])
            clause_summary = item.get("summary") or item.get("clause", "")

            if isinstance(risks, str):
                risks = [risks]

            filtered = []
            for r in risks:
                if isinstance(r, str) and "no major risk" not in r.lower():
                    filtered.append(r)

            if filtered:
                risk_lines.append(f"Clause {i}: {clause_summary[:200]}")
                for r in filtered:
                    risk_lines.append(f"  - {r}")

        if not risk_lines:
            return "No major risky clauses were detected by the system."

        return "Risky clauses / issues found:\n\n" + "\n".join(risk_lines)

    def _answer_rights_laws(self, clauses):
        if not clauses:
            return "No legal rights information was extracted from the document."

        lines = []
        for i, item in enumerate(clauses[:6], start=1):
            laws = item.get("laws", [])
            summary = item.get("summary") or item.get("clause", "")

            if isinstance(laws, str):
                laws = [laws]

            if laws:
                lines.append(f"Clause {i}: {summary[:180]}")
                for law in laws:
                    lines.append(f"  - {law}")

        if not lines:
            return "No specific legal rights or laws were matched for this document."

        return "Relevant rights / legal guidance from the document:\n\n" + "\n".join(lines)

    def _answer_next_steps(self, clauses):
        if not clauses:
            return "No next-step guidance is available because no clauses were extracted."

        steps = []
        for item in clauses:
            next_steps = item.get("next_steps", [])

            if isinstance(next_steps, str):
                next_steps = [next_steps]

            for step in next_steps:
                if step and step not in steps:
                    steps.append(step)

        if not steps:
            return "No next steps were generated for this document."

        final_steps = steps[:8]
        return "Suggested next steps based on this document:\n\n" + "\n".join(
            [f"{i}. {step}" for i, step in enumerate(final_steps, start=1)]
        )

    def _search_clause_by_keywords(self, clauses, keywords, fallback_message):
        if not clauses:
            return fallback_message

        matched = []

        for i, item in enumerate(clauses, start=1):
            clause_text = item.get("clause", "").lower()
            summary = item.get("summary", "").lower()
            explanation = item.get("explanation", "").lower()

            full_text = f"{clause_text} {summary} {explanation}"

            if any(k.lower() in full_text for k in keywords):
                display = item.get("summary") or item.get("explanation") or item.get("clause", "")
                matched.append(f"Clause {i}: {display[:300]}")

        if matched:
            return "I found the following relevant parts in the document:\n\n" + "\n\n".join(matched[:5])

        return fallback_message

    def _smart_keyword_search(self, question_lower, clauses):
        if not clauses:
            return None

        # Extract useful words from question
        words = re.findall(r"[a-zA-Z]+", question_lower)
        words = [w for w in words if len(w) > 3]

        if not words:
            return None

        matched = []

        for i, item in enumerate(clauses, start=1):
            clause_text = item.get("clause", "").lower()
            summary = item.get("summary", "").lower()
            explanation = item.get("explanation", "").lower()

            combined = f"{clause_text} {summary} {explanation}"

            score = 0
            for word in words:
                if word in combined:
                    score += 1

            if score > 0:
                display = item.get("summary") or item.get("explanation") or item.get("clause", "")
                matched.append((score, f"Clause {i}: {display[:300]}"))

        if not matched:
            return None

        matched.sort(reverse=True, key=lambda x: x[0])
        top_matches = [m[1] for m in matched[:4]]

        return "Based on your question, these parts of the document are most relevant:\n\n" + "\n\n".join(top_matches)