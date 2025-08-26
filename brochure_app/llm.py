from __future__ import annotations
import os
from typing import Generator, Optional, Iterable, Any
from dotenv import load_dotenv

def stream_gpt(user_prompt: str,
               system_prompt: Optional[str] = None,
               model: Optional[str] = None,
               client: Optional[Any] = None) -> Generator[str, None, None]:
    """Stream tokens from an OpenAI-compatible Chat Completions API.

    - If `client` is None, constructs `openai.OpenAI()` using env var OPENAI_API_KEY.
    - Uses `model` from env `OPENAI_MODEL` if not provided.
    - Yields cumulative text chunks (suitable for Gradio streaming).

    For unit tests, pass a fake `client` whose `chat.completions.create(..., stream=True)`
    yields objects with `.choices[0].delta.content`.
    """
    load_dotenv(override=True)
    model = model or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    system = system_prompt or "You are a helpful assistant."

    if client is None:
        try:
            from openai import OpenAI
        except Exception as e:
            raise RuntimeError("openai package not installed; install openai to use stream_gpt without a mock client") from e
        client = OpenAI()

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_prompt},
    ]

    full = ""
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        stream=True,
    )

    for chunk in stream:
        try:
            piece = chunk.choices[0].delta.content or ""
        except Exception:
            piece = ""
        if piece:
            full += piece
            yield full  # cumulative for nicer UX
