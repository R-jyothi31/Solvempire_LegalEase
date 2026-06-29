import streamlit as st
import os
import sys

# --------------------------------------------------
# Add Project Root
# --------------------------------------------------
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# --------------------------------------------------
# Import Rights Agent
# --------------------------------------------------
from agents.rights_law_agent import get_rights

# --------------------------------------------------
# Check Session
# --------------------------------------------------
if "analysis_complete" not in st.session_state:
    st.session_state.analysis_complete = False

if not st.session_state.analysis_complete:
    st.warning("⚠️ Please upload a document first.")
    st.stop()

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Legal Rights — LegalEase",
    page_icon="⚖️",
    layout="wide"
)

css_path = os.path.join(BASE_DIR, "frontend", "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --------------------------------------------------
# Extra page-level styles (next_steps palette)
# --------------------------------------------------
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

/* ── Clause body ── */
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

/* ── rec-section / rec-point / rec-dot ── */
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

# --------------------------------------------------
# Page Title
# --------------------------------------------------
st.markdown("""
<h1>⚖️ Legal Rights Analysis</h1>
<p class='page-subtitle'>AI-identified rights and entitlements from your document</p>
""", unsafe_allow_html=True)

st.markdown("---")

# --------------------------------------------------
# Document Info Card
# --------------------------------------------------
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

# --------------------------------------------------
# Rights Analysis Button
# --------------------------------------------------
st.markdown('<div class="section-strip">⚖️ Rights Identification</div>', unsafe_allow_html=True)

if st.button("🔍 Identify Legal Rights", use_container_width=False):
    with st.spinner("Analyzing legal rights…"):
        rights = get_rights(st.session_state.document_text)
        st.session_state.rights = rights

# --------------------------------------------------
# Display Rights
# --------------------------------------------------
if st.session_state.get("rights"):

    rights_text = st.session_state.rights

    # Split into individual points and render as styled cards
    lines = [l.strip().lstrip("-•*►▸1234567890. ").strip()
             for l in rights_text.splitlines() if l.strip()]

    if lines:
        html = '<div class="rec-section"><h4>⚖️ Your Legal Rights</h4>'
        for i, line in enumerate(lines, start=1):
            html += f"""
            <div class="rec-point">
                <div class="rec-dot">{i}</div>
                <span>{line}</span>
            </div>"""
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div class="clause-body" style="border-left:4px solid var(--gold);">'
            f'{rights_text}</div>',
            unsafe_allow_html=True
        )

st.markdown("---")

# --------------------------------------------------
# Navigation
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("⬅ Back to FAQ", use_container_width=True):
        st.switch_page("pages/faq.py")

with col2:
    if st.button("Next ➜ Risk Analysis", use_container_width=True):
        st.switch_page("pages/risk.py")