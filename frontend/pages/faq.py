import streamlit as st
from utils import answer_faq_question

st.title("FAQ Section")
st.write("Ask questions about the uploaded legal document.")

analysis_result = st.session_state.get("analysis_result", None)

if not analysis_result:
    st.warning("Please upload and analyze a document first.")
    st.stop()

st.subheader("Quick FAQs")

faq_options = [
    "What type of document is this?",
    "Summarize the clauses for me",
    "What are the risky clauses?",
    "What are the next steps?",
    "Who are the parties in this document?"
]

selected_faq = st.selectbox("Choose a FAQ", faq_options)

if st.button("Get FAQ Answer"):
    answer = answer_faq_question(selected_faq, analysis_result)
    st.markdown("### Answer")
    st.write(answer)

st.subheader("Ask Your Own Question")
user_question = st.text_input("Type your question")

if st.button("Get My Answer"):
    if user_question.strip():
        answer = answer_faq_question(user_question, analysis_result)
        st.markdown("### Answer")
        st.write(answer)
    else:
        st.warning("Please enter a question.")