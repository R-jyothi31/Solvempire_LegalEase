# LegalEase
## AI Legal Document Assistant using RAG + Multi-Agent AI

LegalEase is an AI-powered legal document assistant designed to help common users understand legal documents such as **consumer complaints, rental agreements, employment contracts, NDAs, lease agreements, and legal notices** in a simple and understandable way.

The system uses **RAG (Retrieval-Augmented Generation)** and **multiple AI agents** to analyze uploaded legal PDFs, extract clauses, retrieve relevant legal rights, explain legal language in simple English/Telugu, detect risky clauses, and suggest next steps for the user.

---

# 1. Project Overview

Legal documents are often written in complex legal language, making them difficult for normal users to understand. People may sign agreements, receive notices, or file complaints without clearly knowing:

- what the document says
- what rights they have
- what risky clauses are present
- what action they should take next

**LegalEase** solves this problem by acting as an **AI legal assistant** that reads uploaded legal documents and converts them into **simple, structured, and user-friendly legal guidance**.

---

# 2. Problem Statement

Many people interact with legal documents without understanding the actual meaning of clauses, obligations, rights, penalties, or legal consequences. This creates confusion and can lead to poor decisions.

LegalEase addresses this by building an **end-to-end legal document analysis system** that can:

- read legal PDF documents
- identify the document type
- extract and summarize important clauses
- retrieve relevant laws and rights
- explain clauses in simple language
- flag risky or unfair clauses
- suggest what the user can do next

---

# 3. Solution Provided by LegalEase

To solve the above problem, we built a **RAG + Multi-Agent AI system**.

## Our solution pipeline:
1. **Collect legal documents** such as consumer rights laws, employment agreements, rental agreements, and legal notices.
2. **Convert PDFs to text** using a PDF loader.
3. **Chunk the text** into smaller legal passages.
4. **Generate embeddings** for each chunk.
5. **Store embeddings in ChromaDB / FAISS** for retrieval.
6. **Upload a legal PDF** through the Streamlit frontend.
7. **Document Parser Agent** detects document type and extracts clauses.
8. **Rights Agent** retrieves relevant legal rights/laws for each clause.
9. **Explainer Agent** converts legal language into simple English/Telugu.
10. **Risk Agent** flags risky or suspicious clauses.
11. **Next Steps Agent** suggests practical actions such as filing a complaint, negotiating a clause, consulting a lawyer, or contacting authorities.
12. **FAQ / Ask Your Own Question** allows users to interact with the analyzed document.

---

# 4. Key Features

- Upload legal PDF documents
- Automatic document type detection
- Clause extraction from legal documents
- Legal clause explanation in simple language
- Relevant rights and law mapping
- Risky clause detection
- Next-step legal suggestions
- Clause-by-clause analysis
- FAQ support for uploaded documents
- Ask-your-own-question support
- English / Telugu-friendly explanation flow
- Streamlit-based easy user interface

---

# 5. Types of Documents Supported

LegalEase is designed to work with:

## Consumer Rights Documents
- Consumer Protection Act
- Consumer Protection Rules
- E-Commerce Consumer Rules
- Consumer Complaint formats
- Consumer rights guides

## Rental / Lease Documents
- Rental agreements
- House lease agreements
- PG agreements
- Apartment rental documents

## Employment Documents
- Employment agreements
- Internship agreements
- Offer letters
- Non-Disclosure Agreements (NDA)
- Service agreements

## Legal Notices
- Consumer complaint notices
- Property notices
- Payment recovery notices

---

# 6. How We Solved the Project

The project was implemented in stages.

## Step 1: Legal Data Collection
We collected legal PDF documents from official and public legal sources such as:
- India Code
- Department of Consumer Affairs
- eCourts / legal notice resources
- public legal agreement templates

The documents were organized into categories:
- consumer laws
- rental agreements
- employment contracts
- legal notices

---

## Step 2: PDF to Text Conversion
We created a PDF loader using **PyMuPDF** to extract text from each legal PDF.

This helps convert raw legal documents into machine-readable text.

---

## Step 3: Chunking
Long legal documents were split into smaller chunks so that:
- embeddings could be generated properly
- relevant sections could be retrieved faster
- clause-based analysis becomes easier

---

## Step 4: Embedding Generation
Each chunk was converted into vector embeddings using **HuggingFace sentence-transformer embeddings**.

These embeddings represent the semantic meaning of the legal text.

---

## Step 5: Vector Storage
The embeddings were stored in **ChromaDB / FAISS** so that the system can perform semantic retrieval when answering legal questions.

---

## Step 6: Agent Development
We created multiple agents to perform specific legal analysis tasks:

### Document Parser Agent
- detects document type
- extracts clauses / sections from the document

### Rights Agent
- retrieves relevant laws and rights
- maps clauses with possible legal rights

### Explainer Agent
- converts complex legal language into simple English/Telugu

### Risk Agent
- identifies risky, unfair, or suspicious clauses

### Next Steps Agent
- suggests actions such as:
  - file a complaint
  - negotiate a clause
  - keep proof of payment
  - consult a lawyer
  - contact consumer authorities

### FAQ Agent
- answers common and custom questions about the uploaded document

---

## Step 7: Full Workflow Integration
All the agents were integrated into a single **LegalWorkflow pipeline** so that once a user uploads a document, the system performs:

**Upload → Parse → Clause Extraction → Rights Mapping → Explanation → Risk Detection → Next Steps → FAQ**

---

## Step 8: Frontend Development
We built the frontend using **Streamlit** with multiple pages:
- Upload page
- Analysis page
- Clause View page
- Rights page
- FAQ page

This makes the system easy to use even for non-technical users.

---

# 7. Project Architecture / Workflow Summary

The LegalEase system follows this flow:

1. User uploads a legal PDF
2. PDF text is extracted
3. Document type is identified
4. Clauses are extracted
5. Rights/laws are retrieved from vector database
6. Clauses are simplified
7. Risks are flagged
8. Next steps are suggested
9. User can ask FAQs or their own questions

---

# 8. Tech Stack

## Programming & Core Tools
- Python

## Frontend
- Streamlit

## RAG / AI Framework
- LangChain

## Vector Database
- ChromaDB / FAISS

## Embedding Model
- HuggingFace Sentence Transformers

## PDF Processing
- PyMuPDF (`fitz`)

## LLM / API
- OpenAI API / Gemini API

## Utilities
- dotenv
- os / json / regex / pathlib

---

# 9. Project Folder Structure

```bash
LegalEase/
│
├── data/
│   ├── raw/
│   │   ├── consumer_laws/
│   │   ├── rental_agreements/
│   │   ├── employment_contracts/
│   │   └── legal_notices/
│   │
│   ├── processed/
│   │   ├── texts/
│   │   ├── chunks/
│   │   └── embeddings/
│
├── vector_store/
│   └── chromadb/
│
├── agents/
│   ├── __init__.py
│   ├── document_parser_agent.py
│   ├── rights_agent.py
│   ├── explainer_agent.py
│   ├── risk_agent.py
│   ├── next_steps_agent.py
│   ├── faq_agent.py
│   └── legal_workflow.py
│
├── rag/
│   ├── __init__.py
│   ├── pdf_loader.py
│   ├── chunker.py
│   ├── embedding.py
│   ├── vector_store.py
│   └── retriever.py
│
├── frontend/
│   ├── app.py
│   ├── utils.py
│   └── pages/
│       ├── upload.py
│       ├── analysis.py
│       ├── clause.py
│       ├── rights.py
│       └── faq.py
│
├── tests/
│   ├── test_rag.py
│   ├── test_agents.py
│   ├── test_pipeline.py
│   └── test_ui.py
│
├── docs/
│   ├── architecture.png
│   ├── workflow.png
│   ├── report_content.txt
│   └── demo_script.txt
│
├── requirements.txt
├── README.md
└── .gitignore