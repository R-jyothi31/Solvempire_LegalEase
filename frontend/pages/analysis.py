import os
import sys
import streamlit as st

# --------------------------------------------------
# Add Project Root
# --------------------------------------------------
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Analysis — LegalEase",
    page_icon="📄",
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

/* ── Stat cards ── */
.stat-card {
    background: #FFFFFF;
    border: 1px solid #BBDEFB;
    border-left: 5px solid #1E88E5;
    border-radius: 10px;
    padding: 1.1rem 1.4rem;
    box-shadow: 0 2px 10px rgba(13,27,42,0.07);
    margin-bottom: 0.5rem;
}
.stat-value {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #0B3D91;
    line-height: 1.2;
}
.stat-label {
    font-size: 0.78rem;
    color: #718096;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 0.2rem;
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

/* ── Summary panel ── */
.summary-panel {
    background: #FFFFFF;
    border: 1px solid #BBDEFB;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    box-shadow: 0 2px 10px rgba(13,27,42,0.06);
}
.summary-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.42rem 0;
    border-bottom: 1px solid #E3F2FD;
    font-size: 0.91rem;
    color: #0B3D91;
}
.summary-row:last-child { border-bottom: none; }
.summary-key {
    color: #718096;
    font-weight: 500;
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ── Text preview box ── */
.text-preview-box {
    background: #F5FAFF;
    border: 1px solid #BBDEFB;
    border-left: 5px solid #1E88E5;
    border-radius: 8px;
    padding: 1.2rem 1.5rem;
    font-size: 0.88rem;
    color: #4A5568;
    line-height: 1.7;
    max-height: 260px;
    overflow-y: auto;
    white-space: pre-wrap;
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

/* ── Empty state ── */
.empty-state {
    background: #E3F2FD;
    border: 1px solid #1E88E5;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    color: #4A5568;
    font-size: 0.95rem;
    text-align: center;
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
# Session Guard
# --------------------------------------------------
if not st.session_state.get("analysis_complete", False):
    st.warning("⚠️ Please upload and analyse a document first.")
    if st.button("Go to Upload"):
        st.switch_page("pages/upload.py")
    st.stop()

# --------------------------------------------------
# Pull values
# --------------------------------------------------
uploaded_file = st.session_state.get("uploaded_file", "Unknown")
document_type = st.session_state.get("document_type", "Unknown")
language      = st.session_state.get("language",      "Unknown")
document_text = st.session_state.get("document_text", "")
clauses       = st.session_state.get("clauses",       [])

word_count = len(document_text.split())
char_count = len(document_text)
line_count = len(document_text.splitlines())

# --------------------------------------------------
# Page Title
# --------------------------------------------------
st.markdown("""
<h1 style='margin-bottom:0'>📄 Document Analysis</h1>
<p class='page-subtitle'>Full breakdown of your uploaded legal document</p>
""", unsafe_allow_html=True)

st.markdown("---")

# --------------------------------------------------
# Stat Cards
# --------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
stats = [
    (str(len(clauses)), "Clauses Found"),
    (f"{word_count:,}",  "Total Words"),
    (f"{char_count:,}",  "Characters"),
    (f"{line_count:,}",  "Lines"),
]
for col, (val, label) in zip([c1, c2, c3, c4], stats):
    with col:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{val}</div>
            <div class="stat-label">{label}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --------------------------------------------------
# Meta + Summary side by side
# --------------------------------------------------
col_left, col_right = st.columns([1.6, 1], gap="large")

with col_left:
    st.markdown('<div class="section-strip">📁 File Information</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="meta-card">
        <div class="meta-row">
            <span class="meta-label">File Name</span>
            <span class="meta-value">{uploaded_file}</span>
        </div>
        <div class="meta-row">
            <span class="meta-label">Document Type</span>
            <span class="badge-type">{document_type}</span>
        </div>
        <div class="meta-row">
            <span class="meta-label">Language</span>
            <span class="badge-lang">{language}</span>
        </div>
        <div class="meta-row">
            <span class="meta-label">Clauses</span>
            <span class="meta-value">{len(clauses)}</span>
        </div>
        <div class="meta-row">
            <span class="meta-label">Word Count</span>
            <span class="meta-value">{word_count:,} words</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="section-strip">📋 Quick Summary</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="summary-panel">
        <div class="summary-row">
            <span class="summary-key">Type</span>
            <span>{document_type}</span>
        </div>
        <div class="summary-row">
            <span class="summary-key">Language</span>
            <span>{language}</span>
        </div>
        <div class="summary-row">
            <span class="summary-key">Clauses</span>
            <span>{len(clauses)}</span>
        </div>
        <div class="summary-row">
            <span class="summary-key">Words</span>
            <span>{word_count:,}</span>
        </div>
        <div class="summary-row">
            <span class="summary-key">Characters</span>
            <span>{char_count:,}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --------------------------------------------------
# Text Preview
# --------------------------------------------------
st.markdown('<div class="section-strip">📜 Extracted Text Preview</div>', unsafe_allow_html=True)

preview = document_text[:3000] + ("…" if len(document_text) > 3000 else "")
st.markdown(
    f'<div class="text-preview-box">{preview}</div>',
    unsafe_allow_html=True
)

with st.expander("📖 View Full Document Text"):
    st.text_area("Full Text", document_text, height=350,
                 label_visibility="collapsed")

st.markdown("---")

# --------------------------------------------------
# Extracted Clauses
# --------------------------------------------------
st.markdown('<div class="section-strip">📑 Extracted Clauses</div>', unsafe_allow_html=True)

if not clauses:
    st.markdown('<div class="empty-state">No clauses were extracted from this document.</div>',
                unsafe_allow_html=True)
else:
    search_term = st.text_input(
        "search", placeholder="🔍 Search clauses by keyword…",
        label_visibility="collapsed"
    )

    filtered = [
        (i, c) for i, c in enumerate(clauses, start=1)
        if not search_term or search_term.lower() in c.lower()
    ]

    st.markdown(
        f"<p style='color:rgb(103, 112, 129);font-size:0.84rem;margin-bottom:0.6rem'>"
        f"Showing <strong>{len(filtered)}</strong> of "
        f"<strong>{len(clauses)}</strong> clauses</p>",
        unsafe_allow_html=True
    )

    for i, clause in filtered:
        preview_label = clause[:80].replace("\n", " ") + "…"
        with st.expander(f"Clause {i}  —  {preview_label}"):
            st.markdown(
                f'<div class="clause-body">{clause}</div>',
                unsafe_allow_html=True
            )
            btn1, btn2 = st.columns(2)
            with btn1:
                if st.button("⚖️ View Rights", key=f"r_{i}"):
                    st.session_state.selected_clause        = clause
                    st.session_state.selected_clause_number = i
                    st.switch_page("pages/rights.py")
            with btn2:
                if st.button("⚠️ Check Risks", key=f"rk_{i}"):
                    st.session_state.selected_clause        = clause
                    st.session_state.selected_clause_number = i
                    st.switch_page("pages/risk.py")

st.markdown("---")

# --------------------------------------------------
# Navigation
# --------------------------------------------------
n1, n2, n3 = st.columns(3)
with n1:
    if st.button("⬅ Back to Upload", use_container_width=True):
        st.switch_page("pages/upload.py")
with n2:
    if st.button("⚖️ View Rights", use_container_width=True):
        st.switch_page("pages/rights.py")
with n3:
    if st.button("Next ➜ FAQ", use_container_width=True):
        st.switch_page("pages/faq.py")