from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

TEXT_FOLDER = "data/processed/texts"
CHUNK_FOLDER = "data/processed/chunks"

os.makedirs(CHUNK_FOLDER, exist_ok=True)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)


def split_text_into_chunks(text):
    """
    Split a single text string into chunks.
    Used in tests and reusable in other files.
    """
    if not text or not text.strip():
        return []

    chunks = splitter.split_text(text)
    return chunks


def process_all_text_files():
    """
    Read all .txt files from data/processed/texts
    and create chunk files in data/processed/chunks
    """
    if not os.path.exists(TEXT_FOLDER):
        print(f"Text folder not found: {TEXT_FOLDER}")
        return

    for file in os.listdir(TEXT_FOLDER):
        if file.endswith(".txt"):
            file_path = os.path.join(TEXT_FOLDER, file)

            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            chunks = split_text_into_chunks(text)

            for i, chunk in enumerate(chunks):
                chunk_filename = file.replace(".txt", f"_chunk_{i}.txt")
                chunk_path = os.path.join(CHUNK_FOLDER, chunk_filename)

                with open(chunk_path, "w", encoding="utf-8") as chunk_file:
                    chunk_file.write(chunk)

            print(f"Chunked: {file} -> {len(chunks)} chunks")

    print("Chunking Complete")


if __name__ == "__main__":
    process_all_text_files()