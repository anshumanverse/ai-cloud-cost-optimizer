
import os
import time
import logging
from typing import Any, Dict, Union
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
logger = logging.getLogger(__name__)


# Environment + Model Setup
HF_API_KEY = os.getenv("HF_API_KEY")
if not HF_API_KEY:
    raise RuntimeError("HF_API_KEY missing in .env")

MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"

# client instance
client = InferenceClient(model=MODEL_NAME, token=HF_API_KEY)


# Internal helpers
def to_str(x):
    """Converts LLM output to string."""
    if x is None:
        return ""
    if isinstance(x, bytes):
        return x.decode("utf-8", errors="ignore")
    return str(x)


def extract_text(resp: Any) -> str:
    """Extract text content from various response formats."""

    # ---- Case 1: dict response with 'choices' ----
    if isinstance(resp, dict):
        choices = resp.get("choices")
        if isinstance(choices, list) and choices:
            first = choices[0]
            if isinstance(first, dict):
                if isinstance(first.get("message"), dict):
                    content = first["message"].get("content")
                    if content:
                        return to_str(content)

                
                for key in ("text", "content", "generated_text"):
                    if key in first:
                        return to_str(first[key])

        
        for key in ("generated_text", "content", "text"):
            if key in resp:
                return to_str(resp[key])

    # ---- Case 2: list response ----
    if isinstance(resp, (list, tuple)) and resp:
        first = resp[0]
        if isinstance(first, dict):
            for key in ("generated_text", "text", "content"):
                if key in first:
                    return to_str(first[key])
        return to_str(first)

    # ---- Case 3: SDK object with .choices ----
    if hasattr(resp, "choices"):
        choices = getattr(resp, "choices", None)
        if choices and len(choices) > 0:
            c0 = choices[0]
            if hasattr(c0, "message") and getattr(c0.message, "content", None):
                return to_str(c0.message.content)
            if hasattr(c0, "text"):
                return to_str(c0.text)

    # ---- Fallback ----
    return to_str(resp)


# Public Chat API
def call_hf_chat(
    prompt: str,
    max_tokens: int = 600,
    temperature: float = 0.0,
    retries: int = 2,
    wait_sec: float = 1.0,
    system_instruction: str = (
        "You are an assistant that MUST output only valid JSON. "
        "Do not return explanations or commentary."
    ),
):
    """
    Send structured chat request to the HF Inference API.
    
    Returns:
        Clean string output (model text only)

    Raises:
        RuntimeError after exhausting retries.
    """

    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": prompt},
    ]

    params = {
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    attempt = 0
    last_exc = None

    while attempt <= retries:
        try:
            # chat_completion preferred
            if hasattr(client, "chat_completion"):
                resp = client.chat_completion(messages=messages, **params)

            # fallback chat()
            elif hasattr(client, "chat"):
                resp = client.chat(messages=messages, **params)

            # worst-case: text_generation
            else:
                resp = client.text_generation(prompt, **params)

            # Normalize and return final text
            return extract_text(resp).strip()

        except Exception as e:
            last_exc = e
            attempt += 1
            logger.warning(f"[call_hf_chat] Attempt {attempt} failed: {e}")

            if attempt > retries:
                break

            time.sleep(wait_sec * attempt)

    raise RuntimeError(f"HF chat failed after {retries+1} attempts: {last_exc}")
