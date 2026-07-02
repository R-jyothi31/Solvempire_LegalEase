import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

if not NVIDIA_API_KEY:
    raise ValueError(
        "NVIDIA_API_KEY not found in .env file. "
        "Set NVIDIA_API_KEY in your .env (or environment/secrets) before "
        "starting the app — without it, every page that imports this "
        "module will crash on startup rather than failing gracefully "
        "per-request."
    )

llm = ChatOpenAI(
    model="meta/llama-3.1-70b-instruct",
    api_key=NVIDIA_API_KEY,
    base_url="https://integrate.api.nvidia.com/v1",
    temperature=0.2,
    max_tokens=2048
)
