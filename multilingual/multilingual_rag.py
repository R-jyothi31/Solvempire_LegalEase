from multilingual.language_detector import detect_language
from multilingual.translator import (
    translate_to_english,
    translate_response
)
from llm.rag_chain import ask_legal_question


def multilingual_answer(query):
    """
    Detect language, translate to English if needed,
    run RAG, then translate answer back.
    """

    if not query or not query.strip():
        return "Please enter a valid question."

    language = detect_language(query)

    print("Detected language:", language)

    if language != "en":
        english_query = translate_to_english(query)
    else:
        english_query = query

    answer = ask_legal_question(english_query)

    if language != "en":
        answer = translate_response(answer, language)

    return answer