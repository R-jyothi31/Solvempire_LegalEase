from deep_translator import GoogleTranslator


def translate_to_english(text):
    """
    Translate arbitrary input text (any detected language) into English.
    Used before feeding user input into the RAG/LLM pipeline.
    """
    if not text or not text.strip():
        return text

    try:
        return GoogleTranslator(
            source='auto',
            target='en'
        ).translate(text)
    except Exception as e:
        print(f"[translate_to_english] Translation failed: {e}")
        return text  # fallback: return original text if translation fails


def translate_response(text, target_language):
    """
    Translate an English response back into the user's selected language.

    target_language must be a language CODE (e.g. 'hi', 'te', 'ta'),
    not a display name like 'Hindi'.
    """
    if not text or not text.strip():
        return text

    # If target is English (or empty/None), skip translation entirely
    if not target_language or target_language.lower() == 'en':
        return text

    try:
        return GoogleTranslator(
            source='en',
            target=target_language
        ).translate(text)
    except Exception as e:
        print(f"[translate_response] Translation failed: {e}")
        return text  # fallback: return original English text if translation fails