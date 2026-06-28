import re


DOCUMENT_TYPES = {
    "Rental Agreement": [
        "rent",
        "tenant",
        "landlord",
        "lease",
        "security deposit",
        "premises",
        "monthly rent",
        "vacate"
    ],

    "Employment Contract": [
        "employee",
        "employer",
        "salary",
        "probation",
        "working hours",
        "termination",
        "leave",
        "joining"
    ],

    "Internship Agreement": [
        "intern",
        "internship",
        "stipend",
        "mentor",
        "training",
        "internship period"
    ],

    "Non Disclosure Agreement": [
        "confidential",
        "nda",
        "non disclosure",
        "confidential information",
        "trade secret"
    ],

    "Service Agreement": [
        "service provider",
        "client",
        "services",
        "payment",
        "scope of work"
    ],

    "Legal Notice": [
        "legal notice",
        "hereby",
        "called upon",
        "cause of action",
        "advocate",
        "demand",
        "notice"
    ],

    "Consumer Complaint": [
        "consumer",
        "deficiency",
        "complaint",
        "refund",
        "compensation",
        "consumer protection"
    ]
}


def detect_document_type(filename, text):
    """
    Detect document type using filename + document content.
    """

    filename = filename.lower()
    text = text.lower()

    # ---------- Filename Detection ----------

    if "rental" in filename:
        return "Rental Agreement"

    if "lease" in filename:
        return "Rental Agreement"

    if "employment" in filename:
        return "Employment Contract"

    if "internship" in filename:
        return "Internship Agreement"

    if "nda" in filename:
        return "Non Disclosure Agreement"

    if "service" in filename:
        return "Service Agreement"

    if "notice" in filename:
        return "Legal Notice"

    if "consumer" in filename:
        return "Consumer Complaint"

    # ---------- Content Detection ----------

    scores = {}

    for doc_type, keywords in DOCUMENT_TYPES.items():

        score = 0

        for word in keywords:

            score += len(re.findall(word, text))

        scores[doc_type] = score

    best_match = max(scores, key=scores.get)

    if scores[best_match] == 0:
        return "Unknown Document"

    return best_match


def document_summary(filename, text):
    """
    Basic summary for preview.
    """

    words = text.split()

    summary = " ".join(words[:120])

    return summary + "..."


def document_statistics(text):

    stats = {
        "Characters": len(text),
        "Words": len(text.split()),
        "Lines": len(text.split("\n"))
    }

    return stats