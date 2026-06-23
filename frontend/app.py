import streamlit as st

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)

# -----------------------------
# Custom CSS for better UI
# -----------------------------
st.markdown("""
    <style>
    .main-title {
        font-size: 40px;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 5px;
    }

    .sub-title {
        font-size: 20px;
        color: #374151;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 26px;
        font-weight: 700;
        color: #111827;
        margin-top: 25px;
        margin-bottom: 10px;
    }

    .feature-box {
        background-color: #F9FAFB;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        margin-bottom: 15px;
    }

    .highlight-box {
        background-color: #EFF6FF;
        padding: 18px;
        border-radius: 12px;
        border-left: 6px solid #2563EB;
        margin-bottom: 20px;
    }

    .info-box {
        background-color: #F3F4F6;
        padding: 16px;
        border-radius: 10px;
        border: 1px solid #D1D5DB;
        margin-bottom: 15px;
    }

    .small-text {
        color: #4B5563;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="main-title">⚖️ LegalEase</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">AI Legal Document Assistant for Understanding Agreements, Notices, Consumer Rights, and Legal Clauses in Simple Language</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="highlight-box">
<b>Welcome to LegalEase</b><br><br>
LegalEase is an AI-powered legal document assistant designed to help common people understand legal documents in a simple and clear way.
It can analyze rental agreements, employment contracts, legal notices, consumer complaints, and related legal documents.
The system reads the uploaded document, identifies important clauses, explains them in simple English or Telugu, highlights risky terms,
retrieves related legal rights, and suggests the next steps a user can take.
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Project Overview
# -----------------------------
st.markdown('<div class="section-title">📌 Project Overview</div>', unsafe_allow_html=True)

st.write("""
LegalEase solves a real-world problem: many people sign or receive legal documents without understanding what they actually mean.
Legal language is often complex, technical, and difficult for non-lawyers to interpret. Because of this, students, tenants, employees,
and consumers may unknowingly accept unfair terms or miss important legal rights.

This project uses **RAG (Retrieval-Augmented Generation)** and **multiple AI agents** to make legal documents easier to understand.
The system extracts important clauses from uploaded documents, retrieves relevant legal knowledge from a legal database,
explains the meaning of the clauses in simple words, identifies risky content, and provides actionable next-step guidance.
""")

# -----------------------------
# Problem Statement
# -----------------------------
st.markdown('<div class="section-title">⚠️ Problem Statement</div>', unsafe_allow_html=True)

st.markdown("""
<div class="feature-box">
<ul>
<li>People often sign legal documents such as rental agreements, offer letters, NDAs, and notices without understanding them.</li>
<li>Legal documents contain complex clauses, hidden risks, obligations, and conditions that are difficult for normal users to interpret.</li>
<li>Consumers receiving notices or complaints may not know their legal rights or what action they should take next.</li>
<li>There is a need for a simple AI system that can explain legal documents in plain language and provide useful legal guidance.</li>
</ul>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# What LegalEase Does
# -----------------------------
st.markdown('<div class="section-title">🚀 What LegalEase Does</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-box">
    <b>1. Document Upload & Reading</b><br>
    Upload legal PDF documents such as rental agreements, consumer notices, complaint documents, offer letters, and contracts.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-box">
    <b>2. Document Type Detection</b><br>
    Automatically identifies whether the uploaded file is a rental agreement, employment document, consumer complaint, legal notice, NDA, or a general legal document.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-box">
    <b>3. Clause Extraction</b><br>
    Breaks the document into important clauses or meaningful legal sections so the user can view them one by one.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
    <b>4. Simple Explanation</b><br>
    Converts difficult legal language into easy-to-understand explanations in simple English or Telugu.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-box">
    <b>5. Risk Detection</b><br>
    Highlights risky, unfair, unusual, or harmful clauses such as penalties, lock-in periods, high deposits, or one-sided conditions.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-box">
    <b>6. Legal Rights & Next Steps</b><br>
    Retrieves relevant legal rights and suggests actions such as filing a complaint, negotiating a clause, consulting a lawyer, or contacting authorities.
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Workflow
# -----------------------------
st.markdown('<div class="section-title">🔄 How the System Works</div>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
<b>Step 1:</b> User uploads a legal PDF document.<br><br>
<b>Step 2:</b> The system extracts text from the PDF and identifies the document type.<br><br>
<b>Step 3:</b> Important clauses are extracted from the document.<br><br>
<b>Step 4:</b> Relevant legal rights and laws are retrieved from the legal knowledge base using RAG.<br><br>
<b>Step 5:</b> The clauses are explained in simple language for the user.<br><br>
<b>Step 6:</b> Risky clauses are flagged and the user is given next-step guidance.<br><br>
<b>Step 7:</b> The user can explore clause-wise analysis and ask FAQs about the document.
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Agents
# -----------------------------
st.markdown('<div class="section-title">🤖 AI Agents Used in LegalEase</div>', unsafe_allow_html=True)

st.markdown("""
<div class="feature-box">
<b>Document Parser Agent</b><br>
Detects document type and extracts important clauses from the uploaded legal document.
</div>

<div class="feature-box">
<b>Rights & Law Agent</b><br>
Retrieves relevant legal rights, acts, rules, and legal guidance based on the content of the clause.
</div>

<div class="feature-box">
<b>Explainer Agent</b><br>
Converts difficult legal language into simple and understandable explanations for normal users.
</div>

<div class="feature-box">
<b>Risk Flagging Agent</b><br>
Identifies risky, unfair, or legally sensitive clauses that the user should review carefully.
</div>

<div class="feature-box">
<b>Next Steps Agent</b><br>
Suggests what the user should do next after reading the document, such as negotiating a clause, filing a complaint, or seeking legal help.
</div>

<div class="feature-box">
<b>FAQ Agent</b><br>
Answers user questions about the uploaded document, such as main points, risky clauses, laws involved, and next actions.
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Supported Document Types
# -----------------------------
st.markdown('<div class="section-title">📂 Supported Document Types</div>', unsafe_allow_html=True)

st.markdown("""
<div class="feature-box">
<ul>
<li>Consumer Complaints and Consumer Rights Documents</li>
<li>Rental Agreements and Lease Agreements</li>
<li>Employment Contracts and Offer Letters</li>
<li>Internship Agreements</li>
<li>Non-Disclosure Agreements (NDA)</li>
<li>Legal Notices such as Property Notices or Payment Recovery Notices</li>
<li>General Legal Documents</li>
</ul>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar Usage
# -----------------------------
st.markdown('<div class="section-title">📌 Use the Sidebar</div>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
Use the sidebar to navigate through the LegalEase system:
<ul>
<li><b>Upload</b> – Upload your legal PDF document</li>
<li><b>Analysis</b> – View overall document analysis</li>
<li><b>Clause View</b> – See clause-by-clause explanation, risks, laws, and next steps</li>
<li><b>FAQ</b> – Ask questions about the uploaded legal document</li>
</ul>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Tech Stack
# -----------------------------
st.markdown('<div class="section-title">🛠️ Tech Stack</div>', unsafe_allow_html=True)

st.markdown("""
<div class="feature-box">
<ul>
<li><b>Frontend:</b> Streamlit</li>
<li><b>Backend:</b> Python</li>
<li><b>RAG Framework:</b> LangChain / LlamaIndex</li>
<li><b>Vector Database:</b> ChromaDB</li>
<li><b>Embeddings:</b> Sentence Transformers / HuggingFace Embeddings</li>
<li><b>PDF Processing:</b> PyMuPDF / pdfplumber</li>
<li><b>LLM:</b> Gemini / OpenAI model</li>
</ul>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("LegalEase • AI Legal Document Assistant • Built using RAG + Agentic AI")