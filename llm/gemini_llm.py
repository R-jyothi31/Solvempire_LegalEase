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

BASE_URL = "https://integrate.api.nvidia.com/v1"
_primary_override = os.getenv("NVIDIA_MODEL_NAME")

MODEL_CANDIDATES = [
    m for m in [
        _primary_override,                          
        "nvidia/nemotron-3-ultra-550b-a55b",         
        "deepseek-ai/deepseek-v4-flash-0731",        
        "nvidia/nemotron-3.5-lightning-30b-a3b",     
        "moonshotai/kimi-k3",                        
    ] if m
]


class ResilientNvidiaLLM:

    def __init__(self, model_candidates, api_key, base_url, temperature=0.2, max_tokens=2048):
        if not model_candidates:
            raise ValueError("No NVIDIA model candidates configured.")
        self._candidates = model_candidates
        self._api_key = api_key
        self._base_url = base_url
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._working_index = 0

    def _build_client(self, model_name):
        return ChatOpenAI(
            model=model_name,
            api_key=self._api_key,
            base_url=self._base_url,
            temperature=self._temperature,
            max_tokens=self._max_tokens,
        )

    @staticmethod
    def _is_retired_error(e: Exception) -> bool:
        error_str = str(e).lower()
        return (
            "410" in str(e)
            or "end of life" in error_str
            or "no longer available" in error_str
        )

    def invoke(self, prompt):
        last_error = None

        for i in range(self._working_index, len(self._candidates)):
            model_name = self._candidates[i]
            try:
                client = self._build_client(model_name)
                response = client.invoke(prompt)
                if i != self._working_index:
                    print(f"[gemini_llm] Switched to fallback model: {model_name}")
                self._working_index = i  
                return response
            except Exception as e:
                last_error = e
                if self._is_retired_error(e):
                    print(f"[gemini_llm] Model '{model_name}' has been retired, "
                          f"trying next candidate: {e}")
                    continue
                
                raise

       
        raise RuntimeError(
            f"All configured NVIDIA models have been retired or are "
            f"unavailable: {self._candidates}. Check "
            f"https://build.nvidia.com/models for currently live 'Free "
            f"Endpoint' models and update MODEL_CANDIDATES in "
            f"llm/gemini_llm.py. Last error: {last_error}"
        )


llm = ResilientNvidiaLLM(
    model_candidates=MODEL_CANDIDATES,
    api_key=NVIDIA_API_KEY,
    base_url=BASE_URL,
)
