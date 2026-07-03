from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

# Fix: makes langdetect deterministic across runs
DetectorFactory.seed = 0


LANGUAGE_MAP = {
    "en": "English",
    "te": "Telugu",
    "hi": "Hindi",
    "ta": "Tamil",
    "kn": "Kannada",
    "ml": "Malayalam",
    "mr": "Marathi",
    "bn": "Bengali",
    "gu": "Gujarati",
    "pa": "Punjabi",
    "ur": "Urdu",
    "or": "Odia"
}


def detect_language(text):
    """
    Detect the language of the uploaded document.
    """

    if not text or len(text.strip()) == 0:
        return "Unknown"

    # Guard: use only first 2000 chars for faster, stable detection
    sample = text.strip()[:2000]

    try:
        code = detect(sample)
        return LANGUAGE_MAP.get(code, code)

    except LangDetectException:
        return "Unknown"