import streamlit as st
import os
import sys

# --------------------------------------------------
# Add Project Root
# --------------------------------------------------
BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Legal Recommendations — LegalEase",
    page_icon="✅",
    layout="wide"
)

# --------------------------------------------------
# Load CSS
# --------------------------------------------------
css_path = os.path.join(BASE_DIR, "frontend", "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --------------------------------------------------
# Extra page-level styles
# --------------------------------------------------
st.markdown("""
<style>
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
.rec-point:last-child {
    border-bottom: none;
}
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
.section-header-strip {
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
.doc-meta-card {
    background: #FFFFFF;
    border: 1px solid #BBDEFB;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    box-shadow: 0 2px 10px rgba(13,27,42,0.06);
}
.doc-meta-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.45rem 0;
    border-bottom: 1px solid #E3F2FD;
    font-size: 0.92rem;
}
.doc-meta-row:last-child { border-bottom: none; }
.doc-meta-label {
    color: #718096;
    font-weight: 500;
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.doc-meta-value {
    color: #0B3D91;
    font-weight: 600;
    font-size: 0.92rem;
}
.badge-doctype {
    background: #E3F2FD;
    color: #0B3D91;
    border: 1px solid #1E88E5;
    border-radius: 99px;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 3px 14px;
}
.checklist-item {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 0.5rem 0;
    color: #4A5568;
    font-size: 0.93rem;
    border-bottom: 1px solid #E3F2FD;
}
.checklist-item:last-child { border-bottom: none; }
.check-icon {
    color: #1A6B4A;
    font-size: 1rem;
    font-weight: 700;
}
.nav-btn-container {
    display: flex;
    gap: 1rem;
    margin-top: 2rem;
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
# Import Agent
# --------------------------------------------------
from agents.next_steps_agent import (
    suggest_next_steps,
    generate_checklist,
    emergency_actions
)

# --------------------------------------------------
# Session Guard
# --------------------------------------------------
if not st.session_state.get("analysis_complete", False):
    st.warning("⚠️ Please upload and analyze a document first.")
    if st.button("Go to Upload"):
        st.switch_page("pages/upload.py")
    st.stop()

# --------------------------------------------------
# Pull session values
# --------------------------------------------------
uploaded_file   = st.session_state.get("uploaded_file", "Unknown")
document_type   = st.session_state.get("document_type", "Unknown")
language        = st.session_state.get("language", "Unknown")
clauses         = st.session_state.get("clauses", [])
document_text   = st.session_state.get("document_text", "")

# --------------------------------------------------
# Page Title
# --------------------------------------------------
st.markdown("""
<h1 style='margin-bottom:0'>✅ Legal Recommendations</h1>
<p style='color:#718096;font-size:0.95rem;margin-top:0.3rem'>
    AI-generated action plan based on your uploaded document
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# --------------------------------------------------
# Two-column layout: meta left, checklist right
# --------------------------------------------------
col_left, col_right = st.columns([1.4, 1], gap="large")

with col_left:
    st.markdown('<div class="section-header-strip">📄 Document Information</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="doc-meta-card">
        <div class="doc-meta-row">
            <span class="doc-meta-label">File Name</span>
            <span class="doc-meta-value">{uploaded_file}</span>
        </div>
        <div class="doc-meta-row">
            <span class="doc-meta-label">Document Type</span>
            <span class="badge-doctype">{document_type}</span>
        </div>
        <div class="doc-meta-row">
            <span class="doc-meta-label">Language</span>
            <span class="doc-meta-value">{language}</span>
        </div>
        <div class="doc-meta-row">
            <span class="doc-meta-label">Total Clauses</span>
            <span class="doc-meta-value">{len(clauses)}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="section-header-strip">✅ Document Checklist</div>', unsafe_allow_html=True)
    checklist = generate_checklist({"document_type": document_type})
    checklist_html = '<div class="doc-meta-card">'
    for item in checklist:
        checklist_html += f"""
        <div class="checklist-item">
            <span class="check-icon">✓</span>
            <span>{item}</span>
        </div>"""
    checklist_html += "</div>"
    st.markdown(checklist_html, unsafe_allow_html=True)

st.markdown("---")

# --------------------------------------------------
# Emergency Actions
# --------------------------------------------------
urgent = emergency_actions(document_type)
if urgent:
    st.markdown('<div class="section-header-strip">🚨 Urgent Actions</div>', unsafe_allow_html=True)
    urgent_html = '<div class="rec-section"><h4>Take These Steps Immediately</h4>'
    for i, action in enumerate(urgent, start=1):
        urgent_html += f"""
        <div class="rec-point">
            <div class="rec-dot">{i}</div>
            <span>{action}</span>
        </div>"""
    urgent_html += "</div>"
    st.markdown(urgent_html, unsafe_allow_html=True)

st.markdown("---")

# --------------------------------------------------
# AI Recommendations Button
# --------------------------------------------------
st.markdown('<div class="section-header-strip">🤖 AI Legal Recommendations</div>', unsafe_allow_html=True)

if st.button("⚡ Generate AI Recommendations", use_container_width=True):
    with st.spinner("Analyzing your document and generating recommendations..."):
        try:
            document = {
                "document_type": document_type,
                "clauses": clauses
            }
            recommendations = suggest_next_steps(document)
            st.session_state.next_steps = recommendations
        except Exception as e:
            st.error(f"Error generating recommendations: {str(e)}")

# --------------------------------------------------
# Display Recommendations — point by point
# --------------------------------------------------
if st.session_state.get("next_steps"):

    recommendations = st.session_state.next_steps

    # Section keywords to auto-group points
    SECTIONS = {
        "📋 Overall Summary":        ["summary", "overview", "document"],
        "🔖 Recommended Next Steps": ["step", "next", "recommend", "action", "should"],
        "📁 Documents Required":     ["document", "required", "need", "submit", "attach"],
        "⚠️ Precautions":            ["precaution", "caution", "avoid", "ensure", "warning"],
        "⚖️ Legal Advice":           ["legal", "law", "right", "court", "advocate", "lawyer"],
        "🏛️ Government Authority":   ["authority", "government", "forum", "consumer", "ministry"],
        "👨‍⚖️ Lawyer Consultation":   ["lawyer", "consult", "attorney", "legal expert"],
    }

    # Bucket each line into sections
    bucketed = {s: [] for s in SECTIONS}
    uncategorized = []

    for line in recommendations:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Strip leading bullets/numbers
        clean = line.lstrip("-•*►▸1234567890. ").strip()
        if not clean:
            continue

        matched = False
        lower = clean.lower()
        for section, keywords in SECTIONS.items():
            if any(kw in lower for kw in keywords):
                bucketed[section].append(clean)
                matched = True
                break
        if not matched:
            uncategorized.append(clean)

    # Render each section that has content
    for section_title, points in bucketed.items():
        if not points:
            continue
        html = f'<div class="rec-section"><h4>{section_title}</h4>'
        for i, point in enumerate(points, start=1):
            html += f"""
            <div class="rec-point">
                <div class="rec-dot">{i}</div>
                <span>{point}</span>
            </div>"""
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)

    # Render any uncategorized points
    if uncategorized:
        html = '<div class="rec-section"><h4>📌 Additional Points</h4>'
        for i, point in enumerate(uncategorized, start=1):
            html += f"""
            <div class="rec-point">
                <div class="rec-dot">{i}</div>
                <span>{point}</span>
            </div>"""
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)

else:
    st.markdown("""
    <div style='background:#E3F2FD;border:1px solid #1E88E5;border-radius:10px;
                padding:1.2rem 1.5rem;color:#4A5568;font-size:0.95rem;text-align:center;'>
        Click <strong>Generate AI Recommendations</strong> above to get your personalized legal action plan.
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --------------------------------------------------
# Navigation
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("⬅ Back to Risk Analysis", use_container_width=True):
        st.switch_page("pages/risk.py")

with col2:
    if st.button("🔄 Analyze Another Document", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.switch_page("pages/upload.py")