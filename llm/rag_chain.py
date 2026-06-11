from rag.retriever import retrieve
from llm.gemini_llm import llm


def ask_legal_question(question):

    docs = retrieve(question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are a legal document assistant.

Answer only using the context.

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    return response.content