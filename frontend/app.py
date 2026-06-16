import streamlit as st
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)
from llm.rag_chain import ask_legal_question

st.title("⚖️ LegalEase")

question = st.text_input(
    "Ask a Legal Question"
)

if st.button("Submit"):

    answer = ask_legal_question(question)

    st.write(answer)
