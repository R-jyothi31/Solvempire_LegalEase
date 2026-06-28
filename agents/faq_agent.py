# faq_agent.py

from llm.gemini_llm import llm  # Add at top of file


class FAQAgent:
    def answer_question(self, question, analysis_result):

        if not analysis_result:
            return "No document analysis found. Please upload and analyze a document first."

        question = str(question).strip().lower()
        document_type = analysis_result.get("document_type", "Unknown Document")
        clauses = analysis_result.get("analysis", [])

        if not clauses:
            return f"This document is identified as: {document_type}, but no clauses were extracted for analysis."

        # ... all your existing keyword blocks stay exactly as they are ...

        # -----------------------------
        # 8. Fallback — LLM answers unknown questions
        # -----------------------------
        clause_texts = []
        for item in clauses[:5]:
            clause_text = str(item.get("clause", "")).replace("\n", " ").strip()
            clause_text = " ".join(clause_text.split())
            clause_texts.append(clause_text[:300])

        relevant_clauses = "\n".join(clause_texts)

        prompt = (
            "You are an AI Legal Assistant.\n\n"
            f"Document Type: {document_type}\n\n"
            "Relevant Clauses:\n"
            f"{relevant_clauses}\n\n"
            "Answer this question based on the document:\n"
            f"{question}"
        )

        try:
            response = llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"Could not answer: {str(e)}"