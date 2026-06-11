import streamlit as st

st.title("🛡 Consumer Rights")

rights = [
    "Right to Safety",
    "Right to Information",
    "Right to Choose",
    "Right to be Heard",
    "Right to Seek Redressal",
    "Right to Consumer Education"
]

for right in rights:
    st.success(right)