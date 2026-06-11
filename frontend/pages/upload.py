import streamlit as st
import os

UPLOAD_FOLDER = "data/raw/uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

st.title("📄 Upload Legal Document")

uploaded_file = st.file_uploader(
    "Choose PDF",
    type=["pdf"]
)

if uploaded_file:

    save_path = os.path.join(
        UPLOAD_FOLDER,
        uploaded_file.name
    )

    with open(save_path, "wb") as f:
        f.write(
            uploaded_file.getbuffer()
        )

    st.success(
        f"{uploaded_file.name} uploaded successfully."
    )

    st.write(
        f"Saved at: {save_path}"
    )