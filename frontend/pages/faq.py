import streamlit as st
from utils import answer_faq_question

st.title("FAQ Section")
st.write("Ask questions about the uploaded legal document.")

analysis_result = st.session_state.get("analysis_result")

if not analysis_result:
    st.warning("Please upload and analyze a document first.")
    st.stop()

faq_options = [
    "What type of document is this?",
    "What is this document about?",
    "What are the main points?",
    "Are there any risky clauses?",
    "Which laws apply?",
    "What should I do next?"
]

selected_faq = st.selectbox("Choose a FAQ", faq_options)

if st.button("Get Answer"):
    answer = answer_faq_question(selected_faq, analysis_result)
    st.subheader("Answer")
    st.write(answer)

st.markdown("---")
st.subheader("Ask Your Own Question")

custom_question = st.text_input("Type your question")

if st.button("Ask Question"):
    if custom_question.strip():
        answer = answer_faq_question(custom_question, analysis_result)
        st.subheader("Answer")
        st.write(answer)
    else:
        st.warning("Please enter a question.")