import re


def clean_clause(text):
    """
    Clean extracted clause text.
    """
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_clauses(text):
    """
    Extract clauses from legal documents.

    Supports formats like:

    Clause 1
    CLAUSE 2
    Section 3
    1.
    1.1
    ARTICLE I
    """

    if not text:
        return []

    patterns = [

        r"(?=Clause\s+\d+)",

        r"(?=CLAUSE\s+\d+)",

        r"(?=Section\s+\d+)",

        r"(?=SECTION\s+\d+)",

        r"(?=\n\d+\.)",

        r"(?=\n\d+\.\d+)",

        r"(?=ARTICLE\s+[IVXLC]+)",

        r"(?=Article\s+[IVXLC]+)"
    ]

    clauses = None

    for pattern in patterns:

        parts = re.split(pattern, text)

        if len(parts) > 1:

            clauses = parts

            break

    if clauses is None:
        return [clean_clause(text)]

    results = []

    for clause in clauses:

        clause = clean_clause(clause)

        if len(clause) > 30:
            results.append(clause)

    return results


def get_clause_titles(clauses):
    """
    Create titles for navigation.
    """

    titles = []

    for i, clause in enumerate(clauses):

        first_line = clause[:60]

        titles.append(
            {
                "id": i + 1,
                "title": first_line + "..."
            }
        )

    return titles


def search_clause(keyword, clauses):
    """
    Search clauses by keyword.
    """

    keyword = keyword.lower()

    matched = []

    for i, clause in enumerate(clauses):

        if keyword in clause.lower():

            matched.append(
                {
                    "clause_number": i + 1,
                    "text": clause
                }
            )

    return matched


def clause_statistics(clauses):

    total_words = 0

    total_characters = 0

    for clause in clauses:

        total_words += len(clause.split())

        total_characters += len(clause)

    return {

        "Total Clauses": len(clauses),

        "Total Words": total_words,

        "Total Characters": total_characters
    }