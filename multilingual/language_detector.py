from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

DetectorFactory.seed = 0


def detect_language(text):
    """
    Detect language code from text. Returns 'en' as fallback.
    """
    if not text or len(text.strip()) == 0:
        return "en"

    try:
        return detect(text.strip()[:2000])
    except LangDetectException:
        return "en"