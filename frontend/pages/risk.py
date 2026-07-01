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
# Import Risk Agent
# --------------------------------------------------
from agents.risk_flagging_agent import flag_risks

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
    page_title="Risk Analysis — LegalEase",
    page_icon="⚠️",
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

/* ── Risk level badges ── */
.badge-risk-high {
    background: #FFF5F5;
    color: #C53030;
    border: 1px solid #FC8181;
    border-radius: 99px;
    font-size: 0.78rem;
    font-weight: 700;
    padding: 3px 14px;
}
.badge-risk-medium {
    background: #FFFAF0;
    color: #C05621;
    border: 1px solid #F6AD55;
    border-radius: 99px;
    font-size: 0.78rem;
    font-weight: 700;
    padding: 3px 14px;
}
.badge-risk-low {
    background: #F0FFF4;
    color: #276749;
    border: 1px solid #68D391;
    border-radius: 99px;
    font-size: 0.78rem;
    font-weight: 700;
    padding: 3px 14px;
}

/* ── Clause body ── */
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

/* ── rec-section / rec-point / rec-dot ── */
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

# --------------------------------------------------
# Page Title
# --------------------------------------------------
st.markdown("""
<h1>⚠️ Risk Analysis</h1>
<p class='page-subtitle'>AI-flagged risky clauses and potential legal issues</p>
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
# Risk Analysis Button
# --------------------------------------------------
st.markdown('<div class="section-strip">⚠️ Risk Detection</div>', unsafe_allow_html=True)

if st.button("🔍 Analyze Risks", use_container_width=False):
    with st.spinner("Finding risky clauses…"):
        risks = flag_risks(st.session_state.document_text)
        st.session_state.risks = risks

# --------------------------------------------------
# Display Risks + Risk Level
# --------------------------------------------------
if st.session_state.get("risks"):

    risks_text = st.session_state.risks
    risk_lower = risks_text.lower()

    # Risk level badge
    if "high" in risk_lower:
        level_html = '<span class="badge-risk-high">🔴 High Risk</span>'
        level      = "high"
    elif "medium" in risk_lower:
        level_html = '<span class="badge-risk-medium">🟠 Medium Risk</span>'
        level      = "medium"
    else:
        level_html = '<span class="badge-risk-low">🟢 Low Risk</span>'
        level      = "low"

    # Risk level card
    st.markdown(f"""
    <div class="meta-card" style="margin-bottom:1rem;">
        <div class="meta-row">
            <span class="meta-label">Overall Risk Level</span>
            {level_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Risk report — split into points
    st.markdown('<div class="section-strip">📋 Risk Report</div>', unsafe_allow_html=True)

    lines = [l.strip().lstrip("-•*►▸1234567890. ").strip()
             for l in risks_text.splitlines() if l.strip()]

    if lines:
        # Choose left border colour based on risk level
        border_color = (
            "var(--danger)"  if level == "high"   else
            "var(--warning)" if level == "medium"  else
            "var(--success)"
        )
        html = f'<div class="rec-section" style="border-left-color:{border_color};"><h4>Identified Risks</h4>'
        for i, line in enumerate(lines, start=1):
            html += f"""
            <div class="rec-point">
                <div class="rec-dot" style="background:{border_color};color:#fff;">{i}</div>
                <span>{line}</span>
            </div>"""
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div class="clause-body" style="border-left:4px solid blue;">'
            f'{risks_text}</div>',
            unsafe_allow_html=True
        )

st.markdown("---")

# --------------------------------------------------
# Navigation
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("⬅ Back to Rights", use_container_width=True):
        st.switch_page("pages/rights.py")

with col2:
    if st.button("Next ➜ Recommendations", use_container_width=True):
        st.switch_page("pages/next_steps.py")