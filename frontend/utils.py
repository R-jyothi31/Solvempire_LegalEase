import os
import sys
import re
from difflib import SequenceMatcher

# =========================================================
# PATH SETUP
# =========================================================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))          # frontend/
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))   # project root

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
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# =========================================================
# PDF TEXT EXTRACTION
# =========================================================
def extract_text_from_pdf(file_path):
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
    if not pdf_text or not pdf_text.strip():
        return "Legal Document"

    text = pdf_text.lower()

    document_keywords = {
        "Rental Agreement": [
            "tenant", "landlord", "lease", "rent", "security deposit",
            "premises", "monthly rent", "lease term", "rental agreement",
            "lessor", "lessee", "vacate", "occupancy"
        ],
        "Employment Agreement": [
            "employee", "employer", "salary", "termination", "employment",
            "probation", "job title", "compensation", "working hours",
            "leave policy", "notice period", "appointment", "service"
        ],
        "Consumer Complaint": [
            "consumer complaint", "complaint", "refund", "replacement",
            "defective product", "deficiency in service", "consumer forum",
            "opposite party", "grievance", "invoice", "warranty", "seller",
            "merchant", "damages", "product defect"
        ],
        "Non-Disclosure Agreement": [
            "confidential", "confidential information", "non-disclosure",
            "nda", "receiving party", "disclosing party", "proprietary",
            "trade secret", "confidentiality"
        ],
        "Legal Notice": [
            "legal notice", "you are hereby called upon", "cause of action",
            "advocate", "within 15 days", "within 7 days", "notice is hereby"
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
# SPLIT DOCUMENT INTO CLAUSES
# =========================================================
def split_document_into_clauses(pdf_text):
    if not pdf_text or not pdf_text.strip():
        return []

    text = pdf_text.replace("\r", "\n")

    # 1) numbered clauses
    numbered_matches = list(re.finditer(r'(?m)(?:^|\n)\s*(\d+)\.\s+', text))
    if len(numbered_matches) >= 2:
        clauses = []
        for i, match in enumerate(numbered_matches):
            start = match.start()
            end = numbered_matches[i + 1].start() if i + 1 < len(numbered_matches) else len(text)
            clause = clean_text(text[start:end].strip())
            if len(clause) > 25:
                clauses.append(clause)
        if clauses:
            return clauses

    # 2) ALL CAPS headings
    heading_pattern = r'(?m)(?:^|\n)([A-Z][A-Z\s/&,\-]{3,})\s*(?:\n|:)'
    heading_matches = list(re.finditer(heading_pattern, text))
    if len(heading_matches) >= 2:
        clauses = []
        for i, match in enumerate(heading_matches):
            start = match.start()
            end = heading_matches[i + 1].start() if i + 1 < len(heading_matches) else len(text)
            clause = clean_text(text[start:end].strip())
            if len(clause) > 25:
                clauses.append(clause)
        if clauses:
            return clauses

    # 3) paragraph-based
    paragraphs = re.split(r"\n\s*\n", text)
    clauses = []
    for para in paragraphs:
        para = clean_text(para)
        if len(para) > 80:
            clauses.append(para)

    if clauses:
        return clauses

    # 4) fallback blocks
    words = text.split()
    block_size = 120
    clauses = []
    for i in range(0, len(words), block_size):
        chunk = " ".join(words[i:i + block_size]).strip()
        if len(chunk) > 25:
            clauses.append(chunk)

    return clauses

# =========================================================
# SMALL CLAUSE UNDERSTANDING HELPERS
# =========================================================
def get_clause_topic(clause_text, document_type):
    text = clause_text.lower()

    # Rental
    if document_type == "Rental Agreement":
        if any(k in text for k in ["rent", "monthly rent", "payment"]):
            return "rent"
        if any(k in text for k in ["deposit", "security deposit", "advance"]):
            return "deposit"
        if any(k in text for k in ["term", "lease period", "commencement", "expiry"]):
            return "term"
        if any(k in text for k in ["terminate", "termination", "vacate", "notice"]):
            return "termination"
        if any(k in text for k in ["maintenance", "repair", "damage"]):
            return "maintenance"
        if any(k in text for k in ["use of premises", "premises", "occupy", "sublet"]):
            return "use"

    # Employment
    if document_type == "Employment Agreement":
        if any(k in text for k in ["salary", "wages", "compensation", "pay"]):
            return "salary"
        if any(k in text for k in ["probation"]):
            return "probation"
        if any(k in text for k in ["termination", "resignation", "notice period"]):
            return "termination"
        if any(k in text for k in ["duty", "responsibility", "role", "job title"]):
            return "duties"
        if any(k in text for k in ["leave", "holiday", "working hours"]):
            return "work_conditions"
        if any(k in text for k in ["confidential", "non-compete", "non solicitation"]):
            return "confidentiality"

    # Consumer complaint
    if document_type == "Consumer Complaint":
        if any(k in text for k in ["defect", "defective", "faulty", "damaged"]):
            return "defect"
        if any(k in text for k in ["refund", "return", "replacement"]):
            return "refund"
        if any(k in text for k in ["warranty", "guarantee"]):
            return "warranty"
        if any(k in text for k in ["service", "delay", "deficiency"]):
            return "service_issue"
        if any(k in text for k in ["compensation", "damages", "mental agony"]):
            return "compensation"

    # NDA
    if document_type == "Non-Disclosure Agreement":
        if any(k in text for k in ["confidential information", "confidential"]):
            return "confidential_info"
        if any(k in text for k in ["disclosure", "use of information", "use"]):
            return "use_restriction"
        if any(k in text for k in ["term", "duration", "survive"]):
            return "term"
        if any(k in text for k in ["return", "destroy", "materials"]):
            return "return_materials"

    # Legal notice
    if document_type == "Legal Notice":
        if any(k in text for k in ["payment", "dues", "amount"]):
            return "payment_demand"
        if any(k in text for k in ["breach", "violation", "default"]):
            return "breach"
        if any(k in text for k in ["within 7 days", "within 15 days", "reply"]):
            return "reply_deadline"

    return "general"

# =========================================================
# LAW / EXPLANATION / RISK / NEXT STEP GENERATORS
# =========================================================
def get_relevant_laws(document_type, topic):
    law_map = {
        "Rental Agreement": {
            "rent": [
                {"law_name": "Transfer of Property Act, 1882", "description": "Covers lease obligations, rent payment, and landlord-tenant rights."},
                {"law_name": "State Rent Control Principles", "description": "Useful for checking fairness of rent, notice, and eviction-related terms."}
            ],
            "deposit": [
                {"law_name": "Transfer of Property Act, 1882", "description": "Relevant to lease conditions including deposits and possession."}
            ],
            "termination": [
                {"law_name": "Transfer of Property Act, 1882", "description": "Relevant to termination of lease and notice obligations."},
                {"law_name": "State Tenancy / Rent Control Rules", "description": "Useful for verifying eviction and notice validity."}
            ],
            "maintenance": [
                {"law_name": "Transfer of Property Act, 1882", "description": "Relevant to lessor-lessee obligations relating to property condition and use."}
            ],
            "general": [
                {"law_name": "Transfer of Property Act, 1882", "description": "General law governing lease and tenancy arrangements."}
            ]
        },
        "Employment Agreement": {
            "salary": [
                {"law_name": "Payment of Wages Act, 1936", "description": "Relevant to timely payment of wages and deductions."},
                {"law_name": "Code on Wages, 2019", "description": "Covers wage-related rights and employer obligations."}
            ],
            "termination": [
                {"law_name": "Industrial Disputes Act, 1947", "description": "Relevant in disputes involving termination, retrenchment, or unfair dismissal."},
                {"law_name": "Shops and Establishments Rules", "description": "May apply to notice period, working conditions, and termination practices depending on the establishment."}
            ],
            "work_conditions": [
                {"law_name": "Shops and Establishments Rules", "description": "Relevant to working hours, leave, and employment conditions."}
            ],
            "confidentiality": [
                {"law_name": "Indian Contract Act, 1872", "description": "Relevant to enforceability of confidentiality and contractual obligations."}
            ],
            "general": [
                {"law_name": "Indian Contract Act, 1872", "description": "Governs contractual obligations between employer and employee."}
            ]
        },
        "Consumer Complaint": {
            "defect": [
                {"law_name": "Consumer Protection Act, 2019", "description": "Covers defective goods, deficiency in service, and consumer remedies."}
            ],
            "refund": [
                {"law_name": "Consumer Protection Act, 2019", "description": "Supports claims for refund, replacement, and compensation."}
            ],
            "service_issue": [
                {"law_name": "Consumer Protection Act, 2019", "description": "Relevant to deficiency in service and unfair trade practices."}
            ],
            "compensation": [
                {"law_name": "Consumer Protection Act, 2019", "description": "Relevant for seeking compensation for loss, harassment, or mental agony."}
            ],
            "general": [
                {"law_name": "Consumer Protection Act, 2019", "description": "Primary law for consumer complaints regarding goods and services."}
            ]
        },
        "Non-Disclosure Agreement": {
            "confidential_info": [
                {"law_name": "Indian Contract Act, 1872", "description": "Relevant to enforceability of confidentiality obligations and contractual promises."}
            ],
            "use_restriction": [
                {"law_name": "Indian Contract Act, 1872", "description": "Relevant to misuse of confidential information and contractual breach."}
            ],
            "general": [
                {"law_name": "Indian Contract Act, 1872", "description": "General contract law governing confidentiality agreements."}
            ]
        },
        "Legal Notice": {
            "payment_demand": [
                {"law_name": "Indian Contract Act, 1872", "description": "Relevant where payment or breach arises from a contractual relationship."}
            ],
            "breach": [
                {"law_name": "Indian Contract Act, 1872", "description": "Relevant to breach of obligations and legal consequences."}
            ],
            "general": [
                {"law_name": "Indian Contract Act, 1872", "description": "Often relevant where the notice concerns breach, payment, or contractual obligations."}
            ]
        }
    }

    doc_laws = law_map.get(document_type, {})
    return doc_laws.get(topic, doc_laws.get("general", []))

def get_clause_explanation(clause_text, document_type, topic):
    # Rental Agreement
    if document_type == "Rental Agreement":
        explanations = {
            "rent": "This clause explains the rent amount, when it must be paid, and the tenant’s payment obligation to the landlord.",
            "deposit": "This clause describes the security deposit or advance amount and the conditions attached to holding or returning it.",
            "term": "This clause sets out the lease period, including the start date, end date, or duration of tenancy.",
            "termination": "This clause explains how the rental agreement can end, including notice requirements, vacating obligations, or termination conditions.",
            "maintenance": "This clause explains who is responsible for repairs, upkeep, or damage related to the rented property.",
            "use": "This clause explains how the property may be used and may include restrictions on occupation, subletting, or misuse.",
            "general": "This clause sets out a contractual condition between the landlord and tenant regarding the rental arrangement."
        }
        return explanations.get(topic, explanations["general"])

    # Employment Agreement
    if document_type == "Employment Agreement":
        explanations = {
            "salary": "This clause explains the employee’s salary, compensation structure, or payment terms under the employment arrangement.",
            "probation": "This clause explains the probation period, including evaluation or confirmation conditions during the initial employment stage.",
            "termination": "This clause explains how the employment can end, including resignation, notice period, termination grounds, or employer action.",
            "duties": "This clause describes the employee’s role, duties, responsibilities, or expected scope of work.",
            "work_conditions": "This clause explains working conditions such as office hours, leave, attendance, or related employment rules.",
            "confidentiality": "This clause places confidentiality or restrictive obligations on the employee regarding company information.",
            "general": "This clause sets out a contractual term governing the employer-employee relationship."
        }
        return explanations.get(topic, explanations["general"])

    # Consumer Complaint
    if document_type == "Consumer Complaint":
        explanations = {
            "defect": "This part describes the defect, fault, or problem in the product or service complained of by the consumer.",
            "refund": "This part states the consumer’s request for refund, replacement, or return of the defective product or deficient service.",
            "warranty": "This part refers to warranty-related obligations or failures connected with the product or service.",
            "service_issue": "This part explains the deficiency in service, delay, or improper conduct complained of by the consumer.",
            "compensation": "This part describes the compensation or damages sought for loss, inconvenience, or mental agony.",
            "general": "This part sets out a grievance, demand, or factual issue raised in the consumer complaint."
        }
        return explanations.get(topic, explanations["general"])

    # NDA
    if document_type == "Non-Disclosure Agreement":
        explanations = {
            "confidential_info": "This clause defines what information will be treated as confidential under the agreement.",
            "use_restriction": "This clause restricts how confidential information may be used, shared, or disclosed.",
            "term": "This clause explains the duration of confidentiality obligations or the time period for the agreement.",
            "return_materials": "This clause requires return or destruction of confidential documents or materials after the relationship ends.",
            "general": "This clause sets out a confidentiality-related obligation between the parties."
        }
        return explanations.get(topic, explanations["general"])

    # Legal Notice
    if document_type == "Legal Notice":
        explanations = {
            "payment_demand": "This part demands payment of money, dues, or outstanding obligations from the opposite party.",
            "breach": "This part alleges breach, default, or wrongful conduct by the opposite party.",
            "reply_deadline": "This part gives a deadline within which the opposite party is expected to respond or comply.",
            "general": "This part states a legal demand, grievance, or allegation made through the notice."
        }
        return explanations.get(topic, explanations["general"])

    return "This clause states a legal condition or obligation contained in the uploaded document."

def get_clause_risks(clause_text, document_type, topic):
    text = clause_text.lower()
    risks = []

    # generic risk signals
    if any(k in text for k in ["penalty", "forfeit", "deduction", "liable", "without notice", "immediate termination"]):
        risks.append("This clause contains strict consequences or penalties that should be reviewed carefully.")

    # document-specific
    if document_type == "Rental Agreement":
        if topic == "termination":
            risks.append("Check whether the notice period and eviction-related wording are fair and clearly stated.")
        if topic == "deposit":
            risks.append("Verify whether deposit refund conditions, deductions, and timelines are clearly mentioned.")
        if topic == "rent":
            risks.append("Review late payment charges, escalation clauses, or default consequences carefully.")

    elif document_type == "Employment Agreement":
        if topic == "termination":
            risks.append("Check whether termination grounds and notice period are reasonable and legally compliant.")
        if topic == "salary":
            risks.append("Confirm whether deductions, delayed payment conditions, or variable pay terms are clearly defined.")
        if topic == "confidentiality":
            risks.append("Check if confidentiality or restrictive obligations are too broad or continue for an excessive period.")

    elif document_type == "Consumer Complaint":
        if topic == "refund":
            risks.append("Make sure the requested remedy is clearly stated and supported by bill, invoice, or proof of defect.")
        if topic == "defect":
            risks.append("The complaint should clearly connect the defect with the loss or inconvenience suffered.")

    elif document_type == "Non-Disclosure Agreement":
        if topic in ["confidential_info", "use_restriction"]:
            risks.append("Check whether the confidentiality scope is too broad or lacks clear exceptions.")

    elif document_type == "Legal Notice":
        if topic == "reply_deadline":
            risks.append("The response deadline should be noted carefully to avoid missing the next legal step.")

    # if still empty
    if not risks:
        risks.append("No major legal risk is immediately visible from this clause, but the wording should still be reviewed in context.")

    return risks[:2]

def get_clause_next_steps(clause_text, document_type, topic):
    steps = []

    if document_type == "Rental Agreement":
        if topic == "rent":
            steps = [
                "Check the rent amount, due date, and payment method mentioned in the clause.",
                "Verify whether late payment penalty or escalation terms are reasonable."
            ]
        elif topic == "deposit":
            steps = [
                "Confirm the deposit amount and conditions for refund or deduction.",
                "Keep payment proof and note any damage-related conditions."
            ]
        elif topic == "termination":
            steps = [
                "Check the required notice period before vacating or terminating the tenancy.",
                "Compare termination wording with your agreed rental terms."
            ]
        else:
            steps = [
                "Read this clause together with rent, deposit, and termination clauses for full context."
            ]

    elif document_type == "Employment Agreement":
        if topic == "salary":
            steps = [
                "Check salary structure, pay cycle, and deduction terms carefully.",
                "Verify whether allowances, bonuses, or probation salary changes are mentioned."
            ]
        elif topic == "termination":
            steps = [
                "Check notice period and resignation/termination conditions before signing or accepting the clause.",
                "Compare the clause with your appointment terms and company policy."
            ]
        else:
            steps = [
                "Review this clause with salary, notice period, and work-condition clauses together."
            ]

    elif document_type == "Consumer Complaint":
        steps = [
            "Keep invoice, screenshots, warranty card, and other proof supporting this complaint point.",
            "Ensure the relief requested in the complaint matches the defect or service issue described."
        ]

    elif document_type == "Non-Disclosure Agreement":
        steps = [
            "Check what information is treated as confidential and for how long the obligation continues.",
            "Review any restrictions on use, disclosure, or return of materials."
        ]

    elif document_type == "Legal Notice":
        steps = [
            "Note the deadline mentioned in the notice and gather relevant supporting documents.",
            "Consider responding or seeking legal advice if the notice alleges breach or demands payment."
        ]

    if not steps:
        steps = ["Review this clause carefully along with the surrounding clauses in the document."]

    return steps[:2]

# =========================================================
# BUILD CLAUSE ANALYSIS WITH SMALL MATTER
# =========================================================
def build_clause_analysis_from_pdf(pdf_text, document_type="Legal Document"):
    clauses = split_document_into_clauses(pdf_text)
    analysis = []

    for clause in clauses:
        topic = get_clause_topic(clause, document_type)
        laws = get_relevant_laws(document_type, topic)
        explanation = get_clause_explanation(clause, document_type, topic)
        risks = get_clause_risks(clause, document_type, topic)
        next_steps = get_clause_next_steps(clause, document_type, topic)

        analysis.append({
            "clause": clause,
            "laws": laws,
            "explanation": explanation,
            "risks": risks,
            "next_steps": next_steps
        })

    return analysis

# =========================================================
# RUN LEGAL WORKFLOW SAFELY
# =========================================================
def run_legal_workflow(file_path):
    if legal_pipeline is None:
        return {
            "document_type": "Unknown",
            "analysis": []
        }

    # Case 1: LegalWorkflow class
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

    # Case 2: standalone functions
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
# ENRICH BACKEND ANALYSIS IF IT IS EMPTY / GENERIC
# =========================================================
def enrich_existing_analysis(analysis, document_type):
    """
    If backend already gives clauses but laws/explanation/risks/steps are empty,
    enrich them with small useful matter.
    """
    enriched = []

    for item in analysis:
        clause = str(item.get("clause", "")).strip()
        if not clause:
            continue

        topic = get_clause_topic(clause, document_type)

        laws = item.get("laws", [])
        explanation = str(item.get("explanation", "")).strip()
        risks = item.get("risks", [])
        next_steps = item.get("next_steps", [])

        # enrich if empty / placeholder
        if not laws:
            laws = get_relevant_laws(document_type, topic)

        if not explanation or explanation.lower() in [
            "clause extracted from uploaded document.",
            "no explanation available."
        ]:
            explanation = get_clause_explanation(clause, document_type, topic)

        if not risks or risks == ["No major risks found."] or risks == "No major risks found.":
            risks = get_clause_risks(clause, document_type, topic)

        if not next_steps or next_steps == ["No next steps available."] or next_steps == "No next steps available.":
            next_steps = get_clause_next_steps(clause, document_type, topic)

        enriched.append({
            "clause": clause,
            "laws": laws,
            "explanation": explanation,
            "risks": risks,
            "next_steps": next_steps
        })

    return enriched

# =========================================================
# ANALYZE DOCUMENT
# =========================================================
def analyze_uploaded_document(file_path):
    pdf_text = extract_text_from_pdf(file_path)

    # Run backend workflow if available
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

    # detect type from PDF
    detected_type = detect_document_type(pdf_text)
    workflow_doc_type = str(result.get("document_type", "")).strip()

    if workflow_doc_type.lower() in ["", "unknown", "none", "legal document"]:
        result["document_type"] = detected_type
    elif workflow_doc_type == "Rental Agreement" and detected_type != "Rental Agreement":
        result["document_type"] = detected_type
    else:
        result["document_type"] = workflow_doc_type

    final_doc_type = result["document_type"]

    analysis = result.get("analysis", [])
    if not isinstance(analysis, list):
        analysis = []

    # If backend returns no clause / one clause, rebuild from PDF
    if len(analysis) <= 1:
        rebuilt = build_clause_analysis_from_pdf(pdf_text, final_doc_type)
        if rebuilt:
            result["analysis"] = rebuilt
    else:
        # enrich existing backend analysis
        result["analysis"] = enrich_existing_analysis(analysis, final_doc_type)

    return result

# =========================================================
# SPLIT PDF INTO SMALL CHUNKS FOR QUESTION ANSWERING
# =========================================================
def split_pdf_into_chunks(pdf_text):
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
    return [chunk for score, chunk in scored_chunks[:top_k] if score > 0]

# =========================================================
# EXTRACT SHORT PRECISE ANSWER
# =========================================================
def extract_precise_answer(question, chunk):
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

    if len(scored_sentences) > 1 and scored_sentences[1][0] > 1.5:
        second_sentence = scored_sentences[1][1]
        if second_sentence != best_sentence:
            return best_sentence + " " + second_sentence

    return best_sentence

# =========================================================
# ANSWER FROM PDF
# =========================================================
def answer_from_pdf(question, analysis_result):
    pdf_text = analysis_result.get("pdf_text", "")

    if not pdf_text.strip():
        return "I could not read the uploaded PDF text properly."

    relevant_chunks = find_relevant_pdf_chunks(question, pdf_text, top_k=1)
    if not relevant_chunks:
        return "I could not find a relevant answer in the uploaded PDF."

    return extract_precise_answer(question, relevant_chunks[0])

# =========================================================
# FAQ / CUSTOM QUESTION ANSWERING
# =========================================================
def answer_faq_question(question, analysis_result):
    question_lower = question.lower().strip()

    # 1) Document type
    if "what type of document" in question_lower:
        return f"This document is identified as: {analysis_result.get('document_type', 'Unknown')}"

    # 2) Summarize clauses
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

    # 3) Risky clauses
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

    # 4) Next steps
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

    # 5) Who are the parties?
    if "who are the parties" in question_lower or "parties in this document" in question_lower:
        return answer_from_pdf(question, analysis_result)

    # 6) Any custom question -> answer from PDF
    return answer_from_pdf(question, analysis_result)