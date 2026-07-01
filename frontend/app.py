import streamlit as st
import os
import sys

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)

# --------------------------------------------------
# Load Global CSS
# --------------------------------------------------
css_path = os.path.join(BASE_DIR, "frontend", "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --------------------------------------------------
# Extra page-level styles (matching next_steps palette)
# --------------------------------------------------
st.markdown("""
<style>
/* ── Page title ── */
h1 {
    font-family: 'Playfair Display', serif;
    color: #0B3D91;
}
.page-subtitle {
    color: black;
    font-size: 0.95rem;
    margin-top: 0.2rem;
}

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
    box-shadow: 0 2px 10px rgba(11,61,145,0.08);
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
    color: black;
    font-weight: 500;
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.meta-value {
    color: black;
    font-weight: 600;
    font-size: 0.92rem;
}

/* ── Feature cards grid ── */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-top: 0.5rem;
    margin-bottom: 1.5rem;
}
.feature-card {
    background: #FFFFFF;
    border: 1px solid #BBDEFB;
    border-left: 5px solid #1E88E5;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    box-shadow: 0 2px 10px rgba(11,61,145,0.08);
    transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.15s ease;
}
.feature-card:hover {
    background: #F5FAFF;
    border-color: #1E88E5;
    box-shadow: 0 6px 16px rgba(11,61,145,0.18);
    transform: translateY(-3px);
}
.feature-icon {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
}
.feature-title {
    font-family: 'Playfair Display', serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: black;
    margin-bottom: 0.3rem;
}
.feature-desc {
    font-size: 0.82rem;
    color: black;
    line-height: 1.55;
}

/* ── Workflow steps ── */
.workflow-strip {
    display: flex;
    gap: 0;
    margin: 0.5rem 0 1.5rem 0;
}
.workflow-step {
    flex: 1;
    background: #FFFFFF;
    border: 1px solid #BBDEFB;
    border-right: none;
    padding: 0.9rem 1rem;
    text-align: center;
}
.workflow-step:first-child { border-radius: 10px 0 0 10px; }
.workflow-step:last-child  { border-radius: 0 10px 10px 0; border-right: 1px solid #BBDEFB; }
.workflow-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 26px;
    height: 26px;
    background: #1E88E5;
    color: #FFFFFF;
    border-radius: 50%;
    font-size: 0.75rem;
    font-weight: 700;
    margin-bottom: 0.4rem;
}
.workflow-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: #0B3D91;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    display: block;
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
    color: black;
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
# Initialize Session State
# --------------------------------------------------
defaults = {
    "analysis_complete": False,
    "uploaded_file":     None,
    "file_path":         "",
    "document_text":     "",
    "language":          "",
    "document_type":     "",
    "clauses":           [],
    "summary":           "",
    "rights":            "",
    "risks":             "",
    "next_steps":        "",
    "documents":         []
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --------------------------------------------------
# Page Title
# --------------------------------------------------
st.markdown("""
<h1 style='margin-bottom:0'>⚖️ LegalEase</h1>
<p class='page-subtitle'>AI-Powered Legal Document Assistant</p>
""", unsafe_allow_html=True)

st.markdown("---")

# --------------------------------------------------
# Workflow Steps
# --------------------------------------------------
st.markdown('<div class="section-strip">🗺️ How It Works</div>', unsafe_allow_html=True)

st.markdown("""
<div class="workflow-strip">
    <div class="workflow-step">
        <div class="workflow-num">1</div>
        <span class="workflow-label">📄 Upload</span>
    </div>
    <div class="workflow-step">
        <div class="workflow-num">2</div>
        <span class="workflow-label">📑 Analysis</span>
    </div>
    <div class="workflow-step">
        <div class="workflow-num">3</div>
        <span class="workflow-label">❓ FAQ</span>
    </div>
    <div class="workflow-step">
        <div class="workflow-num">4</div>
        <span class="workflow-label">⚖️ Rights</span>
    </div>
    <div class="workflow-step">
        <div class="workflow-num">5</div>
        <span class="workflow-label">⚠️ Risks</span>
    </div>
    <div class="workflow-step">
        <div class="workflow-num">6</div>
        <span class="workflow-label">✅ Next Steps</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Feature Cards
# --------------------------------------------------
st.markdown('<div class="section-strip">✨ Features</div>', unsafe_allow_html=True)

st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-icon">📄</div>
        <div class="feature-title">Document Upload</div>
        <div class="feature-desc">Upload legal PDF documents for instant AI-powered processing and text extraction.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🌍</div>
        <div class="feature-title">Multi-language</div>
        <div class="feature-desc">Automatic language detection with support for documents in multiple languages.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">📑</div>
        <div class="feature-title">Clause Extraction</div>
        <div class="feature-desc">Automatically identifies and extracts individual clauses for detailed review.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">⚖️</div>
        <div class="feature-title">Rights Identification</div>
        <div class="feature-desc">AI identifies your legal rights and entitlements within the document.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">⚠️</div>
        <div class="feature-title">Risk Detection</div>
        <div class="feature-desc">Flags potentially risky clauses and assigns High / Medium / Low risk levels.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">💡</div>
        <div class="feature-title">Recommendations</div>
        <div class="feature-desc">AI-generated action plan with next steps, checklists, and urgent actions.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Supported Document Types
# --------------------------------------------------
st.markdown('<div class="section-strip">📁 Supported Document Types</div>', unsafe_allow_html=True)

st.markdown("""
<div class="meta-card" style="max-width:680px;">
    <div class="meta-row">
        <span class="meta-label">🏠 Rental / Lease</span>
        <span class="meta-value">Tenancy agreements, lease deeds</span>
    </div>
    <div class="meta-row">
        <span class="meta-label">💼 Employment</span>
        <span class="meta-value">Offer letters, service agreements</span>
    </div>
    <div class="meta-row">
        <span class="meta-label">🤝 Contracts</span>
        <span class="meta-value">NDAs, vendor &amp; service contracts</span>
    </div>
    <div class="meta-row">
        <span class="meta-label">🏛️ Legal Notices</span>
        <span class="meta-value">Court notices, demand letters</span>
    </div>
    <div class="meta-row">
        <span class="meta-label">🏦 Financial</span>
        <span class="meta-value">Loan agreements, mortgage deeds</span>
    </div>
    <div class="meta-row">
        <span class="meta-label">📋 General</span>
        <span class="meta-value">Any legal or formal PDF document</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --------------------------------------------------
# CTA Button
# --------------------------------------------------
if st.button("🚀 Start Analysis", use_container_width=False):
    st.switch_page("pages/upload.py")