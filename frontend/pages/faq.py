import streamlit as st
import os
import re
import sys

# ----------------------------------------------------
# Add Project Root
# ----------------------------------------------------
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# ----------------------------------------------------
# Import RAG (kept as optional / best-effort — see fallback below)
# ----------------------------------------------------
try:
    from llm.rag_chain import ask_legal_question as rag_ask_legal_question
    RAG_AVAILABLE = True
except Exception:
    RAG_AVAILABLE = False

# ----------------------------------------------------
# Check Session
# ----------------------------------------------------
if "analysis_complete" not in st.session_state:
    st.session_state.analysis_complete = False

if not st.session_state.analysis_complete:
    st.warning("⚠️ Please upload a document first.")
    st.stop()

# ----------------------------------------------------
# Page Config
# ----------------------------------------------------
st.set_page_config(
    page_title="Legal FAQ — LegalEase",
    page_icon="❓",
    layout="wide"
)

css_path = os.path.join(BASE_DIR, "frontend", "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ----------------------------------------------------
# Extra page-level styles (next_steps palette)
# ----------------------------------------------------
st.markdown("""
<style>
/* ── Section strip header ── */
.section-strip {
    background: linear-gradient(90deg, #0B3D91 0%, #1E88E5 100%);
    color: white;
    border-radius: 8px;
    padding: 0.6rem 1.2rem;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 1rem;
    margin-top: 1.5rem;
}

/* ── Meta card ── */
.meta-card {
    background: #FFFFFF;
    border: 1px solid #BBDEFB;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    box-shadow: 0 2px 10px rgba(13,27,42,0.06);
}
.meta-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.45rem 0;
    border-bottom: 1px solid #E3F2FD;
    font-size: 0.92rem;
}
.meta-row:last-child { border-bottom: none; }
.meta-label {
    color: #718096;
    font-weight: 500;
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.meta-value {
    color: #0B3D91;
    font-weight: 600;
    font-size: 0.92rem;
}

/* ── Badges ── */
.badge-type {
    background: #E3F2FD;
    color: #0B3D91;
    border: 1px solid #1E88E5;
    border-radius: 99px;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 3px 14px;
}
.badge-lang {
    background: #EBF4FF;
    color: #1A365D;
    border: 1px solid #90CDF4;
    border-radius: 99px;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 3px 14px;
}

/* ── Clause / answer body ── */
.clause-body {
    background: #F5FAFF;
    border: 1px solid #BBDEFB;
    border-left: 5px solid #1E88E5;
    border-radius: 8px;
    padding: 1rem 1.3rem;
    font-size: 0.9rem;
    color: #4A5568;
    line-height: 1.7;
}

/* ── rec-section / rec-point / rec-dot (shared) ── */
.rec-section {
    background: #FFFFFF;
    border: 1px solid #BBDEFB;
    border-left: 5px solid #1E88E5;
    border-radius: 10px;
    padding: 1.3rem 1.6rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 10px rgba(13,27,42,0.07);
}
.rec-section h4 {
    font-family: 'Playfair Display', serif;
    color: #0B3D91;
    font-size: 1rem;
    margin-bottom: 0.6rem;
    font-weight: 600;
}
.rec-point {
    display: flex;
    align-items: flex-start;
    gap: 0.6rem;
    padding: 0.45rem 0;
    border-bottom: 1px solid #E3F2FD;
    color: #4A5568;
    font-size: 0.93rem;
    line-height: 1.65;
}
.rec-point:last-child { border-bottom: none; }
.rec-dot {
    min-width: 22px;
    height: 22px;
    background: #1E88E5;
    color: #FFFFFF;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.72rem;
    font-weight: 700;
    margin-top: 2px;
}
.rec-dot.risk-high { background: #E74C3C; }
.rec-dot.risk-medium { background: #F1C40F; color: #4A3300; }
.rec-dot.risk-low { background: #2ECC71; }

/* ── Buttons (sky blue / blue) ── */
.stButton > button {
    background: #1E88E5 !important;
    color: #FFFFFF !important;
    border: 1.5px solid #1E88E5 !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
}
.stButton > button:hover {
    background: #0B3D91 !important;
    border-color: #0B3D91 !important;
    color: #E3F2FD !important;
}

/* ── Sidebar nav hover ── */
section[data-testid="stSidebar"] li,
section[data-testid="stSidebar"] a,
[data-testid="stSidebarNav"] li,
[data-testid="stSidebarNav"] a,
[data-testid="stSidebarNavItems"] li,
[data-testid="stSidebarNavItems"] a {
    border-radius: 8px !important;
    transition: background 0.15s ease, color 0.15s ease !important;
}
section[data-testid="stSidebar"] li:hover,
section[data-testid="stSidebar"] a:hover,
[data-testid="stSidebarNav"] li:hover,
[data-testid="stSidebarNav"] a:hover,
[data-testid="stSidebarNavItems"] li:hover,
[data-testid="stSidebarNavItems"] a:hover {
    background: #E3F2FD !important;
    cursor: pointer !important;
}
section[data-testid="stSidebar"] li:hover *,
section[data-testid="stSidebar"] a:hover *,
[data-testid="stSidebarNav"] li:hover *,
[data-testid="stSidebarNav"] a:hover *,
[data-testid="stSidebarNavItems"] li:hover *,
[data-testid="stSidebarNavItems"] a:hover * {
    color: #0B3D91 !important;
}
section[data-testid="stSidebar"] a[aria-current="page"],
[data-testid="stSidebarNav"] a[aria-current="page"],
[data-testid="stSidebarNavItems"] a[aria-current="page"] {
    background: #BBDEFB !important;
}

/* ── General hover (expanders, links) ── */
[data-testid="stExpander"] summary:hover {
    background: #E3F2FD !important;
    color: #1E88E5 !important;
}
a:hover {
    color: #0B3D91 !important;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# Local answer engine (fallback / primary — no external RAG dependency)
# ----------------------------------------------------
RISK_KEYWORDS = {
    "high": [
        "penalty", "penalties", "terminate", "termination", "forfeit",
        "indemnify", "indemnification", "liquidated damages", "breach",
        "non-refundable", "waive", "waiver", "sole discretion",
        "irrevocable", "without notice", "automatically renew"
    ],
    "medium": [
        "late fee", "interest", "notice period", "governing law",
        "jurisdiction", "confidential", "non-compete", "exclusive",
        "arbitration", "dispute"
    ],
    "low": [
        "effective date", "definitions", "signature", "counterpart",
        "entire agreement", "severability"
    ],
}

RIGHTS_KEYWORDS = [
    "entitled to", "may", "has the right to", "reserves the right",
    "peaceful and lawful possession", "refund", "shall be refunded"
]

RESPONSIBILITY_KEYWORDS = [
    "shall", "must", "is required to", "agrees to",
    "responsible for", "shall pay", "shall not"
]

TERMINATION_KEYWORDS = [
    "terminate", "termination", "expire", "expiry", "notice period",
    "vacate", "vacation", "early termination"
]


def classify_clause_risk(clause_text: str) -> str:
    text_lower = clause_text.lower()
    for level in ("high", "medium", "low"):
        for kw in RISK_KEYWORDS[level]:
            if kw in text_lower:
                return level
    return "low"


def _keyword_score(text: str, keywords: list) -> int:
    text_lower = text.lower()
    return sum(text_lower.count(kw) for kw in keywords)


def _clean(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


def local_answer_legal_question(question: str, document_text: str, clauses: list) -> str:
    """Rule-based fallback that always answers from what's actually in the
    document, instead of relying on an external / unavailable RAG chain."""
    q_lower = question.lower().strip()

    # -------- "Explain Clause N" --------
    clause_num_match = re.search(r'clause\s*(\d+)', q_lower)
    if clause_num_match:
        idx = int(clause_num_match.group(1))
        if clauses and 1 <= idx <= len(clauses):
            return f"<strong>Clause {idx}:</strong><br>{_clean(clauses[idx - 1])}"
        return f"I couldn't find Clause {idx} — this document only has {len(clauses)} extracted clause(s)."

    # -------- Risky clauses --------
    if any(w in q_lower for w in ["risky", "risk", "dangerous", "unfair", "concerning"]):
        if not clauses:
            return "No clauses were extracted from this document to assess for risk."
        risky = [(i, c) for i, c in enumerate(clauses, start=1) if classify_clause_risk(c) in ("high", "medium")]
        if not risky:
            return "Based on keyword analysis, no clauses in this document were flagged as high or medium risk."
        lines = "".join(
            f"<div class='rec-point'><div class='rec-dot risk-{classify_clause_risk(c)}'>{i}</div>"
            f"<div><strong>Clause {i}</strong> ({classify_clause_risk(c).upper()} risk): {_clean(c)[:220]}...</div></div>"
            for i, c in risky
        )
        return f"I found <strong>{len(risky)}</strong> clause(s) worth reviewing carefully:<br>{lines}"

    # -------- Rights --------
    if "right" in q_lower:
        hits = [c for c in clauses if _keyword_score(c, RIGHTS_KEYWORDS) > 0]
        if not hits:
            return "I couldn't find explicit rights-related language (e.g. 'entitled to', 'may', 'right to') in the extracted clauses."
        lines = "".join(
            f"<div class='rec-point'><div class='rec-dot'>{i}</div><div>{_clean(c)[:250]}...</div></div>"
            for i, c in enumerate(hits[:6], start=1)
        )
        return f"Here's what the document says about rights:<br>{lines}"

    # -------- Responsibilities / obligations --------
    if any(w in q_lower for w in ["responsib", "obligation", "duty", "duties"]):
        hits = [c for c in clauses if _keyword_score(c, RESPONSIBILITY_KEYWORDS) > 0]
        if not hits:
            return "I couldn't find explicit obligation language (e.g. 'shall', 'must', 'responsible for') in the extracted clauses."
        lines = "".join(
            f"<div class='rec-point'><div class='rec-dot'>{i}</div><div>{_clean(c)[:250]}...</div></div>"
            for i, c in enumerate(hits[:6], start=1)
        )
        return f"Here are the responsibilities/obligations found in the document:<br>{lines}"

    # -------- Termination --------
    if any(w in q_lower for w in ["terminat", "cancel", "end the contract", "end the agreement", "vacate"]):
        hits = [c for c in clauses if _keyword_score(c, TERMINATION_KEYWORDS) > 0]
        if not hits:
            return "I couldn't find explicit termination-related clauses in this document."
        lines = "".join(
            f"<div class='rec-point'><div class='rec-dot'>{i}</div><div>{_clean(c)[:250]}...</div></div>"
            for i, c in enumerate(hits[:6], start=1)
        )
        return f"Here's what the document says about termination:<br>{lines}"

    # -------- Summarize / explain the whole agreement --------
    if any(w in q_lower for w in ["summar", "explain this agreement", "overview", "what is this"]):
        if not clauses:
            preview = _clean(document_text)[:600]
            return f"Document summary (first portion):<br>{preview}..."
        top = clauses[:5]
        lines = "".join(
            f"<div class='rec-point'><div class='rec-dot'>{i}</div><div>{_clean(c)[:220]}...</div></div>"
            for i, c in enumerate(top, start=1)
        )
        return f"This document contains {len(clauses)} clause(s). Here's a summary of the key ones:<br>{lines}"

    # -------- Generic fallback: keyword search across clauses/text --------
    q_words = [w for w in re.findall(r'\w+', q_lower) if len(w) > 3]
    if clauses and q_words:
        scored = []
        for i, c in enumerate(clauses, start=1):
            c_lower = c.lower()
            score = sum(c_lower.count(w) for w in q_words)
            if score > 0:
                scored.append((score, i, c))
        scored.sort(reverse=True, key=lambda x: x[0])
        if scored:
            lines = "".join(
                f"<div class='rec-point'><div class='rec-dot'>{rank}</div>"
                f"<div><strong>Clause {i}</strong>: {_clean(c)[:250]}...</div></div>"
                for rank, (score, i, c) in enumerate(scored[:5], start=1)
            )
            return f"Here's what I found related to your question:<br>{lines}"

    # -------- Absolute last resort: search raw text --------
    if q_words:
        text_lower = document_text.lower()
        for w in q_words:
            pos = text_lower.find(w)
            if pos != -1:
                start = max(0, pos - 150)
                end = min(len(document_text), pos + 250)
                snippet = _clean(document_text[start:end])
                return f"Closest relevant excerpt I found:<br>...{snippet}..."

    return (
        "I couldn't find anything in this document directly answering that. "
        "Try rephrasing, or ask about specific terms like rights, responsibilities, "
        "termination, risky clauses, or a specific clause number."
    )


def ask_legal_question_safe(question: str, filename: str, language: str, document_type: str) -> str:
    """Try the real RAG pipeline first (if available and it returns something
    useful); otherwise fall back to the local, session-state-based answer engine
    so the page never dead-ends on 'No relevant information found.'"""
    document_text = st.session_state.get("document_text", "")
    clauses = st.session_state.get("clauses", [])

    if RAG_AVAILABLE:
        try:
            rag_answer = rag_ask_legal_question(
                question,
                filename=filename,
                language=language,
                document_type=document_type
            )
            if rag_answer and "no relevant information" not in rag_answer.lower():
                return rag_answer
        except Exception:
            pass  # fall through to local engine

    return local_answer_legal_question(question, document_text, clauses)


# ----------------------------------------------------
# Page Title
# ----------------------------------------------------
st.markdown("""
<h1>❓ Legal Questions</h1>
<p class='page-subtitle'>Ask any question about your uploaded document</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ----------------------------------------------------
# Document Info Card
# ----------------------------------------------------
st.markdown('<div class="section-strip">📁 Active Document</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="meta-card">
    <div class="meta-row">
        <span class="meta-label">File Name</span>
        <span class="meta-value">{st.session_state.uploaded_file}</span>
    </div>
    <div class="meta-row">
        <span class="meta-label">Document Type</span>
        <span class="badge-type">{st.session_state.document_type}</span>
    </div>
    <div class="meta-row">
        <span class="meta-label">Language</span>
        <span class="badge-lang">{st.session_state.language}</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------------------------------------------
# Question Input
# ----------------------------------------------------
st.markdown('<div class="section-strip">💬 Ask a Question</div>', unsafe_allow_html=True)

question = st.text_input(
    "question",
    placeholder="e.g. What are my rights under this agreement?",
    label_visibility="collapsed"
)

if st.button("🔍 Get Answer"):

    if question.strip() == "":
        st.warning("⚠️ Please enter a question.")

    else:
        with st.spinner("Searching legal document…"):
            answer = ask_legal_question_safe(
                question,
                filename=st.session_state.uploaded_file,
                language=st.session_state.language,
                document_type=st.session_state.document_type
            )

        st.markdown('<div class="section-strip">🤖 AI Answer</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="clause-body" style="border-left:4px solid #1E88E5;">{answer}</div>',
            unsafe_allow_html=True
        )

st.markdown("---")

# ----------------------------------------------------
# Sample Questions
# ----------------------------------------------------
st.markdown('<div class="section-strip">💡 Example Questions</div>', unsafe_allow_html=True)

examples = [
    "Explain this agreement.",
    "What are the tenant rights?",
    "What are my responsibilities?",
    "Explain Clause 5.",
    "Are there any risky clauses?",
    "What happens if I terminate the contract?",
    "Summarize this document."
]

examples_html = '<div class="meta-card">'
for q in examples:
    examples_html += f"""
    <div class="meta-row" style="justify-content:flex-start;gap:0.6rem;">
        <span style="color:#1E88E5;font-weight:600;font-size:0.9rem;">•</span>
        <span class="meta-value" style="text-align:left;">{q}</span>
    </div>"""
examples_html += "</div>"
st.markdown(examples_html, unsafe_allow_html=True)

st.markdown("---")

# ----------------------------------------------------
# Navigation
# ----------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("⬅ Back to Analysis", use_container_width=True):
        st.switch_page("pages/analysis.py")

with col2:
    if st.button("Next ➜ Rights", use_container_width=True):
        st.switch_page("pages/rights.py")
