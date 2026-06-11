from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

TEXT_FOLDER = "data/processed/texts"
CHUNK_FOLDER = "data/processed/chunks"

os.makedirs(CHUNK_FOLDER, exist_ok=True)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

for file in os.listdir(TEXT_FOLDER):

    if file.endswith(".txt"):

        with open(
            os.path.join(TEXT_FOLDER, file),
            "r",
            encoding="utf-8"
        ) as f:

            text = f.read()

        chunks = splitter.split_text(text)

        for i, chunk in enumerate(chunks):

            filename = file.replace(".txt", f"_chunk_{i}.txt")

            with open(
                os.path.join(CHUNK_FOLDER, filename),
                "w",
                encoding="utf-8"
            ) as chunk_file:

                chunk_file.write(chunk)

print("Chunking Complete")