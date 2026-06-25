import os
import sys
import re
from difflib import SequenceMatcher

# =========================================================
# PATH SETUP
# =========================================================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))          # frontend/
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))   # Solvempire_LegalEase/

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# =========================================================
# IMPORT LEGAL PIPELINE SAFELY
# =========================================================
try:
    import agents.legal_pipeline as legal_pipeline
except Exception:
    legal_pipeline = None

# =========================================================
# UPLOAD FOLDER
# =========================================================
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, "uploaded_docs")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =========================================================
# SAVE UPLOADED FILE
# =========================================================
def save_uploaded_file(uploaded_file):
    """
    Save uploaded file and return saved file path.
    """
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path

# =========================================================
# PDF TEXT EXTRACTION
# =========================================================
def extract_text_from_pdf(file_path):
    """
    Extract text from PDF using PyPDF2.
    """
    try:
        import PyPDF2

        full_text = []
        with open(file_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text.append(page_text)

        return "\n".join(full_text).strip()

    except Exception:
        return ""

# =========================================================
# CLEAN TEXT
# =========================================================
def clean_text(text):
    if not text:
        return ""
    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n+", "\n", text)
    return text.strip()

# =========================================================
# DOCUMENT TYPE DETECTION
# =========================================================
def detect_document_type(pdf_text):
    """
    Detect document type using keyword scoring.
    Prevents every document from becoming Rental Agreement.
    """
    if not pdf_text or not pdf_text.strip():
        return "Legal Document"

    text = pdf_text.lower()

    document_keywords = {
        "Rental Agreement": [
            "tenant", "landlord", "lease", "rent", "security deposit",
            "premises", "monthly rent", "lease term", "rented property",
            "occupancy", "lessor", "lessee", "rental agreement"
        ],
        "Employment Agreement": [
            "employee", "employer", "salary", "termination", "employment",
            "probation", "job title", "compensation", "working hours",
            "leave policy", "notice period", "appointment", "service",
            "employment agreement"
        ],
        "Consumer Complaint": [
            "consumer complaint", "complaint", "refund", "replacement",
            "defective product", "deficiency in service", "consumer forum",
            "opposite party", "grievance", "invoice", "warranty", "seller",
            "merchant", "damages", "product defect", "consumer dispute"
        ],
        "Non-Disclosure Agreement": [
            "confidential", "confidential information", "non-disclosure",
            "nda", "receiving party", "disclosing party", "proprietary",
            "trade secret", "disclosure", "confidentiality"
        ],
        "Legal Notice": [
            "legal notice", "notice is hereby", "under section",
            "you are hereby called upon", "cause of action",
            "advocate", "within 15 days", "within 7 days"
        ]
    }

    scores = {}
    for doc_type, keywords in document_keywords.items():
        score = 0
        for keyword in keywords:
            score += text.count(keyword.lower())
        scores[doc_type] = score

    best_doc_type = max(scores, key=scores.get)
    best_score = scores[best_doc_type]

    if best_score == 0:
        return "Legal Document"

    return best_doc_type

# =========================================================
# SPLIT FULL DOCUMENT INTO CLAUSES
# =========================================================
def split_document_into_clauses(pdf_text):
    """
    Split legal document into clause-like sections.
    This fixes the 'Total Clauses Processed: 1' issue.
    """
    if not pdf_text or not pdf_text.strip():
        return []

    text = pdf_text.replace("\r", "\n")

    # -----------------------------------------------------
    # 1) NUMBERED CLAUSES
    # Example:
    # 1. Term
    # 2. Rent
    # 3. Deposit
    # -----------------------------------------------------
    numbered_matches = list(re.finditer(r'(?m)(?:^|\n)\s*(\d+)\.\s+', text))

    if len(numbered_matches) >= 2:
        clauses = []
        for i, match in enumerate(numbered_matches):
            start = match.start()
            end = numbered_matches[i + 1].start() if i + 1 < len(numbered_matches) else len(text)
            clause = text[start:end].strip()
            clause = clean_text(clause)
            if len(clause) > 25:
                clauses.append(clause)

        if clauses:
            return clauses

    # -----------------------------------------------------
    # 2) ALL CAPS HEADINGS
    # Example:
    # TERM OF LEASE
    # RENT
    # SECURITY DEPOSIT
    # -----------------------------------------------------
    heading_pattern = r'(?m)(?:^|\n)([A-Z][A-Z\s/&,\-]{3,})\s*(?:\n|:)'
    heading_matches = list(re.finditer(heading_pattern, text))

    if len(heading_matches) >= 2:
        clauses = []
        for i, match in enumerate(heading_matches):
            start = match.start()
            end = heading_matches[i + 1].start() if i + 1 < len(heading_matches) else len(text)
            clause = text[start:end].strip()
            clause = clean_text(clause)
            if len(clause) > 25:
                clauses.append(clause)

        if clauses:
            return clauses

    # -----------------------------------------------------
    # 3) SPLIT BY BLANK PARAGRAPHS
    # -----------------------------------------------------
    paragraphs = re.split(r"\n\s*\n", text)
    clauses = []

    for para in paragraphs:
        para = clean_text(para)
        if len(para) > 80:
            clauses.append(para)

    if clauses:
        return clauses

    # -----------------------------------------------------
    # 4) FALLBACK: SPLIT INTO BLOCKS
    # -----------------------------------------------------
    words = text.split()
    block_size = 120
    clauses = []

    for i in range(0, len(words), block_size):
        chunk = " ".join(words[i:i + block_size]).strip()
        if len(chunk) > 25:
            clauses.append(chunk)

    return clauses

# =========================================================
# BUILD CLAUSE ANALYSIS IF BACKEND FAILS
# =========================================================
def build_clause_analysis_from_pdf(pdf_text):
    """
    Build analysis structure from raw PDF clauses if backend analysis is missing.
    """
    clauses = split_document_into_clauses(pdf_text)

    analysis = []
    for clause in clauses:
        analysis.append({
            "clause": clause,
            "laws": [],
            "explanation": "Clause extracted from uploaded document.",
            "risks": [],
            "next_steps": []
        })

    return analysis

# =========================================================
# RUN LEGAL WORKFLOW SAFELY
# =========================================================
def run_legal_workflow(file_path):
    """
    Tries different workflow methods without crashing.
    """
    if legal_pipeline is None:
        return {
            "document_type": "Unknown",
            "analysis": []
        }

    # CASE 1: LegalWorkflow class exists
    if hasattr(legal_pipeline, "LegalWorkflow"):
        try:
            workflow = legal_pipeline.LegalWorkflow()

            possible_methods = [
                "run",
                "analyze_document",
                "process_document",
                "process",
                "execute",
                "analyze"
            ]

            for method_name in possible_methods:
                if hasattr(workflow, method_name):
                    method = getattr(workflow, method_name)
                    if callable(method):
                        try:
                            return method(file_path)
                        except Exception:
                            continue
        except Exception:
            pass

    # CASE 2: standalone functions in legal_pipeline.py
    possible_functions = [
        "analyze_document",
        "run_workflow",
        "process_document",
        "execute_workflow",
        "run"
    ]

    for func_name in possible_functions:
        if hasattr(legal_pipeline, func_name):
            func = getattr(legal_pipeline, func_name)
            if callable(func):
                try:
                    return func(file_path)
                except Exception:
                    continue

    return {
        "document_type": "Unknown",
        "analysis": []
    }

# =========================================================
# ANALYZE DOCUMENT
# =========================================================
def analyze_uploaded_document(file_path):
    """
    Main function used by upload.py.
    - Extracts PDF text
    - Runs workflow if available
    - Fixes wrong document type
    - Fixes clause count if backend returns only one clause
    """
    pdf_text = extract_text_from_pdf(file_path)

    # run workflow
    result = run_legal_workflow(file_path)

    if result is None:
        result = {}

    if not isinstance(result, dict):
        result = {
            "document_type": "Unknown",
            "analysis": []
        }

    result.setdefault("document_type", "Unknown")
    result.setdefault("analysis", [])
    result["pdf_text"] = pdf_text

    # -----------------------------------------------------
    # Fix analysis structure
    # -----------------------------------------------------
    analysis = result.get("analysis", [])

    if not isinstance(analysis, list):
        analysis = []
        result["analysis"] = analysis

    # If backend gives no clauses or only 1 clause, rebuild from PDF
    if len(analysis) <= 1:
        rebuilt_analysis = build_clause_analysis_from_pdf(pdf_text)
        if rebuilt_analysis:
            result["analysis"] = rebuilt_analysis

    # -----------------------------------------------------
    # Fix document type
    # -----------------------------------------------------
    workflow_doc_type = str(result.get("document_type", "")).strip()
    detected_type = detect_document_type(pdf_text)

    # If workflow gives unknown, use detected type
    if workflow_doc_type.lower() in ["", "unknown", "none", "legal document"]:
        result["document_type"] = detected_type

    # If workflow always wrongly says Rental Agreement, override it
    elif workflow_doc_type == "Rental Agreement" and detected_type != "Rental Agreement":
        result["document_type"] = detected_type

    else:
        result["document_type"] = workflow_doc_type

    return result

# =========================================================
# SPLIT PDF INTO SMALL CHUNKS FOR QUESTION ANSWERING
# =========================================================
def split_pdf_into_chunks(pdf_text):
    """
    Split PDF text into small chunks for relevant answer retrieval.
    """
    if not pdf_text:
        return []

    pdf_text = pdf_text.replace("\r", "\n")
    paragraphs = re.split(r"\n\s*\n", pdf_text)
    chunks = []

    for para in paragraphs:
        para = clean_text(para)
        if not para:
            continue

        sentences = re.split(r'(?<=[.!?])\s+', para)
        current_chunk = ""

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            if len(current_chunk) + len(sentence) < 350:
                current_chunk += " " + sentence
            else:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                current_chunk = sentence

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

    return chunks

# =========================================================
# FIND RELEVANT PDF CHUNK
# =========================================================
def find_relevant_pdf_chunks(question, pdf_text, top_k=1):
    """
    Find the most relevant chunk(s) from PDF based on the question.
    """
    chunks = split_pdf_into_chunks(pdf_text)
    if not chunks:
        return []

    question_lower = question.lower().strip()
    question_words = set(re.findall(r"\w+", question_lower))
    scored_chunks = []

    for chunk in chunks:
        chunk_lower = chunk.lower()

        overlap = sum(1 for word in question_words if word in chunk_lower)
        similarity = SequenceMatcher(None, question_lower, chunk_lower[:500]).ratio()

        score = overlap * 3 + similarity
        scored_chunks.append((score, chunk))

    scored_chunks.sort(key=lambda x: x[0], reverse=True)

    best_chunks = [chunk for score, chunk in scored_chunks[:top_k] if score > 0]
    return best_chunks

# =========================================================
# EXTRACT SHORT PRECISE ANSWER
# =========================================================
def extract_precise_answer(question, chunk):
    """
    Return a short answer from the most relevant sentence(s) in the chunk.
    """
    if not chunk:
        return "I could not find a relevant answer in the uploaded PDF."

    question_words = set(re.findall(r"\w+", question.lower()))
    sentences = re.split(r'(?<=[.!?])\s+', chunk)

    scored_sentences = []

    for sent in sentences:
        sent_clean = sent.strip()
        if not sent_clean:
            continue

        sent_lower = sent_clean.lower()
        overlap = sum(1 for word in question_words if word in sent_lower)
        similarity = SequenceMatcher(None, question.lower(), sent_lower).ratio()

        score = overlap * 3 + similarity
        scored_sentences.append((score, sent_clean))

    if not scored_sentences:
        return chunk.strip()

    scored_sentences.sort(key=lambda x: x[0], reverse=True)
    best_sentence = scored_sentences[0][1]

    # add second sentence only if useful
    if len(scored_sentences) > 1 and scored_sentences[1][0] > 1.5:
        second_sentence = scored_sentences[1][1]
        if second_sentence != best_sentence:
            return best_sentence + " " + second_sentence

    return best_sentence

# =========================================================
# ANSWER FROM PDF
# =========================================================
def answer_from_pdf(question, analysis_result):
    """
    Answer custom question directly from uploaded PDF text.
    """
    pdf_text = analysis_result.get("pdf_text", "")

    if not pdf_text.strip():
        return "I could not read the uploaded PDF text properly."

    relevant_chunks = find_relevant_pdf_chunks(question, pdf_text, top_k=1)

    if not relevant_chunks:
        return "I could not find a relevant answer in the uploaded PDF."

    best_chunk = relevant_chunks[0]
    return extract_precise_answer(question, best_chunk)

# =========================================================
# FAQ / CUSTOM QUESTION ANSWERING
# =========================================================
def answer_faq_question(question, analysis_result):
    """
    Handles both quick FAQs and user-typed questions.
    """
    question_lower = question.lower().strip()

    # -----------------------------------------------------
    # 1) DOCUMENT TYPE
    # -----------------------------------------------------
    if "what type of document" in question_lower:
        return f"This document is identified as: {analysis_result.get('document_type', 'Unknown')}"

    # -----------------------------------------------------
    # 2) SUMMARIZE CLAUSES
    # -----------------------------------------------------
    if "summarize the clauses" in question_lower:
        analysis = analysis_result.get("analysis", [])
        if not analysis:
            return "No clause summary is available."

        summary_lines = []
        for i, item in enumerate(analysis[:5], start=1):
            clause_text = item.get("clause", "No clause text available.")
            explanation = item.get("explanation", "No explanation available.")
            summary_lines.append(f"Clause {i}: {clause_text}\nExplanation: {explanation}")

        return "\n\n".join(summary_lines)

    # -----------------------------------------------------
    # 3) RISKY CLAUSES
    # -----------------------------------------------------
    if "risky clauses" in question_lower or "risk" in question_lower:
        analysis = analysis_result.get("analysis", [])
        risky_items = []

        for i, item in enumerate(analysis, start=1):
            risks = item.get("risks", [])

            if isinstance(risks, list) and risks:
                risky_items.append(f"Clause {i}: " + "; ".join(map(str, risks)))
            elif isinstance(risks, str) and risks.strip():
                risky_items.append(f"Clause {i}: {risks}")

        if risky_items:
            return "\n\n".join(risky_items)

        return "No major risks were identified in the analyzed clauses."

    # -----------------------------------------------------
    # 4) NEXT STEPS
    # -----------------------------------------------------
    if "next steps" in question_lower:
        analysis = analysis_result.get("analysis", [])
        steps = []

        for item in analysis:
            next_steps = item.get("next_steps", [])

            if isinstance(next_steps, list):
                steps.extend([str(step) for step in next_steps if str(step).strip()])
            elif isinstance(next_steps, str) and next_steps.strip():
                steps.append(next_steps)

        if steps:
            unique_steps = []
            for step in steps:
                if step not in unique_steps:
                    unique_steps.append(step)

            return "\n".join([f"- {step}" for step in unique_steps])

        return "No next steps are available."

    # -----------------------------------------------------
    # 5) WHO ARE THE PARTIES?
    # -----------------------------------------------------
    if "who are the parties" in question_lower or "parties in this document" in question_lower:
        return answer_from_pdf(question, analysis_result)

    # -----------------------------------------------------
    # 6) ALL OTHER QUESTIONS -> ANSWER FROM PDF
    # -----------------------------------------------------
    return answer_from_pdf(question, analysis_result)