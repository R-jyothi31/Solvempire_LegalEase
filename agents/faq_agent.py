class FAQAgent:
    def answer_question(self, question, analysis_result):
        """
        Answer FAQ or custom user questions based on analyzed document result.
        """

        if not analysis_result:
            return "No document analysis found. Please upload and analyze a document first."

        # -----------------------------
        # Safe conversion
        # -----------------------------
        question = str(question).strip().lower()

        document_type = analysis_result.get("document_type", "Unknown Document")
        clauses = analysis_result.get("analysis", [])

        if not clauses:
            return f"This document is identified as: {document_type}, but no clauses were extracted for analysis."

        # -----------------------------
        # 1. Document type questions
        # -----------------------------
        if any(keyword in question for keyword in [
            "type of document",
            "document type",
            "what document is this",
            "what type is this"
        ]):
            return f"This document is identified as: {document_type}."

        # -----------------------------
        # 2. Document purpose / about
        # -----------------------------
        if any(keyword in question for keyword in [
            "what is this document about",
            "about this document",
            "purpose of this document",
            "what does this document say"
        ]):
            return (
                f"This document is identified as: {document_type}. "
                f"It contains legal terms, responsibilities, conditions, and important clauses related to this document."
            )

        # -----------------------------
        # 3. Summary / main points / clauses
        # -----------------------------
        if any(keyword in question for keyword in [
            "summary",
            "summarize",
            "main points",
            "important points",
            "important clauses",
            "key points",
            "key clauses",
            "summarize the clauses",
            "clause summary",
            "summary of clauses"
        ]):
            summary_lines = []

            for i, item in enumerate(clauses[:5], start=1):
                clause_text = str(item.get("clause", "")).replace("\n", " ").strip()
                clause_text = " ".join(clause_text.split())

                if clause_text:
                    summary_lines.append(f"{i}. {clause_text[:180]}...")

            if summary_lines:
                return (
                    f"Here is a summary of the main clauses from the {document_type}:\n\n"
                    + "\n".join(summary_lines)
                )
            else:
                return "I could not summarize the clauses because no clear clause text was found."

        # -----------------------------
        # 4. Explain clauses in simple words
        # -----------------------------
        if any(keyword in question for keyword in [
            "explain clauses",
            "explain the clauses",
            "simple explanation",
            "explain this document",
            "make it simple",
            "easy explanation"
        ]):
            explanations = []

            for i, item in enumerate(clauses[:3], start=1):
                clause_text = str(item.get("clause", "")).replace("\n", " ").strip()
                clause_text = " ".join(clause_text.split())

                explanation = item.get("explanation", "")

                if isinstance(explanation, dict):
                    explanation_text = explanation.get("simple_explanation", "")
                else:
                    explanation_text = str(explanation)

                if explanation_text:
                    explanations.append(
                        f"Clause {i}:\n"
                        f"Text: {clause_text[:120]}...\n"
                        f"Explanation: {explanation_text}"
                    )

            if explanations:
                return "Simple explanation of important clauses:\n\n" + "\n\n".join(explanations)
            else:
                return "No simplified explanations are available for this document."

        # -----------------------------
        # 5. Risky clauses
        # -----------------------------
        if any(keyword in question for keyword in [
            "risk",
            "risky",
            "danger",
            "unsafe clause",
            "problematic clause",
            "unfair clause"
        ]):
            risky_clauses = []

            for i, item in enumerate(clauses, start=1):
                risks = item.get("risks", "")
                clause_text = str(item.get("clause", "")).replace("\n", " ").strip()
                clause_text = " ".join(clause_text.split())

                if isinstance(risks, list):
                    risks_text = ", ".join([str(r) for r in risks])
                else:
                    risks_text = str(risks)

                if risks_text and "no major risk" not in risks_text.lower():
                    risky_clauses.append(
                        f"Clause {i}: {clause_text[:150]}...\nRisk: {risks_text}"
                    )

            if risky_clauses:
                return "Risky clauses found in this document:\n\n" + "\n\n".join(risky_clauses)
            else:
                return "No major risky clauses were detected in this document."

        # -----------------------------
        # 6. Applicable laws / rights
        # -----------------------------
        if any(keyword in question for keyword in [
            "law",
            "laws",
            "rights",
            "legal rights",
            "applicable laws"
        ]):
            law_lines = []

            for i, item in enumerate(clauses[:5], start=1):
                laws = item.get("laws", "")
                clause_text = str(item.get("clause", "")).replace("\n", " ").strip()
                clause_text = " ".join(clause_text.split())

                if isinstance(laws, list):
                    laws_text = ", ".join([str(l) for l in laws])
                else:
                    laws_text = str(laws)

                if laws_text:
                    law_lines.append(
                        f"Clause {i}: {clause_text[:120]}...\nRelevant Law: {laws_text}"
                    )

            if law_lines:
                return "Relevant laws / rights for this document:\n\n" + "\n\n".join(law_lines)
            else:
                return "No specific legal rights or laws were mapped for this document."

        # -----------------------------
        # 7. Next steps
        # -----------------------------
        if any(keyword in question for keyword in [
            "next step",
            "what should i do",
            "what to do next",
            "action to take",
            "what action should i take"
        ]):
            steps_output = []

            for i, item in enumerate(clauses[:5], start=1):
                steps = item.get("next_steps", "")

                if isinstance(steps, list):
                    steps_text = "\n".join([f"- {s}" for s in steps])
                else:
                    steps_text = str(steps)

                if steps_text.strip():
                    steps_output.append(f"Clause {i}:\n{steps_text}")

            if steps_output:
                return "Suggested next steps based on this document:\n\n" + "\n\n".join(steps_output)
            else:
                return "No next-step guidance is available for this document."

        # -----------------------------
        # 8. Fallback for unknown custom questions
        # -----------------------------
        # Instead of returning only document type, return a useful summary.
        summary_lines = []
        for i, item in enumerate(clauses[:3], start=1):
            clause_text = str(item.get("clause", "")).replace("\n", " ").strip()
            clause_text = " ".join(clause_text.split())
            if clause_text:
                summary_lines.append(f"{i}. {clause_text[:180]}...")

        if summary_lines:
            return (
                f"I could not match the exact question, but here are the key points from the {document_type}:\n\n"
                + "\n".join(summary_lines)
            )

        return f"This document is identified as: {document_type}."