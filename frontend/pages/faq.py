import streamlit as st
import os
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
# Import RAG
# ----------------------------------------------------
from llm.rag_chain import ask_legal_question

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
    background: linear-gradient(90deg, #0D1B2A 0%, #1B2E42 100%);
    color: #C9A84C;
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
    border: 1px solid #E2DAC8;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    box-shadow: 0 2px 10px rgba(13,27,42,0.06);
}
.meta-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.45rem 0;
    border-bottom: 1px solid #F5EDD6;
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
    color: #0D1B2A;
    font-weight: 600;
    font-size: 0.92rem;
}

/* ── Badges ── */
.badge-type {
    background: #F5EDD6;
    color: #0D1B2A;
    border: 1px solid #C9A84C;
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
    background: #FAFAF8;
    border: 1px solid #E2DAC8;
    border-left: 5px solid #C9A84C;
    border-radius: 8px;
    padding: 1rem 1.3rem;
    font-size: 0.9rem;
    color: #4A5568;
    line-height: 1.7;
}

/* ── rec-section / rec-point / rec-dot (shared) ── */
.rec-section {
    background: #FFFFFF;
    border: 1px solid #E2DAC8;
    border-left: 5px solid #C9A84C;
    border-radius: 10px;
    padding: 1.3rem 1.6rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 10px rgba(13,27,42,0.07);
}
.rec-section h4 {
    font-family: 'Playfair Display', serif;
    color: #0D1B2A;
    font-size: 1rem;
    margin-bottom: 0.6rem;
    font-weight: 600;
}
.rec-point {
    display: flex;
    align-items: flex-start;
    gap: 0.6rem;
    padding: 0.45rem 0;
    border-bottom: 1px solid #F5EDD6;
    color: #4A5568;
    font-size: 0.93rem;
    line-height: 1.65;
}
.rec-point:last-child { border-bottom: none; }
.rec-dot {
    min-width: 22px;
    height: 22px;
    background: #C9A84C;
    color: #0D1B2A;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.72rem;
    font-weight: 700;
    margin-top: 2px;
}
</style>
""", unsafe_allow_html=True)

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
            answer = ask_legal_question(
                question,
                filename=st.session_state.uploaded_file,
                language=st.session_state.language,
                document_type=st.session_state.document_type
            )

        st.markdown('<div class="section-strip">🤖 AI Answer</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="clause-body" style="border-left:4px solid var(--gold);">{answer}</div>',
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
    <div class="meta-row">
        <span style="color:#C9A84C;font-weight:600;font-size:0.9rem;">•</span>
        <span class="meta-value" style="text-align:left;max-width:100%;">{q}</span>
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