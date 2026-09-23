"""Shared client factories.

Two chat paths and one embedding path. Pick the one that fits:

    from client import make_chat_client     # OpenCode Go (recommended for new work)
    from client import make_client          # Ollama Cloud (legacy W2/W3/W4 — needs sub)
    from client import make_embedder        # local Ollama (no sub needed; any key works)

Provider history (in order of adoption):
  - 2026-08-26: Ollama Cloud chat + local Ollama embeddings (W2–W4)
  - 2026-09-12: Ollama Cloud Pro subscription ended; OpenCode Go adopted for chat
"""
from __future__ import annotations

import os
import uuid

from dotenv import load_dotenv, find_dotenv
from openai import OpenAI


def make_client() -> OpenAI:
    """Legacy chat client — Ollama Cloud. Requires active Ollama Cloud Pro sub.

    Kept for W2/W3/W4 scripts that imported this. New code should use
    make_chat_client() (OpenCode Go) instead.
    """
    load_dotenv(find_dotenv())
    return OpenAI(
        base_url="https://ollama.com/v1",
        api_key=os.environ["OLLAMA_API_KEY"],
    )


def make_chat_client() -> OpenAI:
    """Chat client — OpenCode Go.

    OpenAI-compatible (uses @ai-sdk/openai-compatible under the hood per
    models.dev). Reads OPENCODE_API_KEY from .env. Base URL is the
    OpenCode Go gateway at https://opencode.ai/zen/go/v1.

    Model names are bare (no 'opencode-go/' prefix): 'kimi-k3',
    'minimax-m3', 'deepseek-v4.1-flash', etc. — the prefix is OpenCode's
    internal namespace and is stripped at the provider boundary.

    IMPORTANT: per https://opencode.ai/docs/go/#where-can-i-use-it, the
    gateway requires two custom headers on every request:
      1. x-opencode-session: a stable session ID for the conversation.
         We generate a UUID once per process and reuse it across all
         requests in that process.
      2. User-Agent: must identify the calling app, NOT a generic SDK
         name like "OpenAI/Python". The default openai-python UA would
         violate this and trigger a 400.
    """
    load_dotenv(find_dotenv())
    return OpenAI(
        base_url="https://opencode.ai/zen/go/v1",
        api_key=os.environ["OPENCODE_API_KEY"],
        default_headers={
            "x-opencode-session": f"llm-practice-{uuid.uuid4().hex[:12]}",
            "User-Agent": "llm-practice/1.0 (midterm-triage)",
        },
    )


"""Client for local Ollama embeddings.

Ollama Cloud has no /v1/embeddings endpoint (probe-verified 2026-09-07:
404 route-not-found), so embeddings run on local Ollama instead.
Local Ollama accepts any non-empty api_key, so the OLLAMA_API_KEY env var
is reused as a placeholder — it does not need to be a valid key.
"""
def make_embedder() -> OpenAI:
    load_dotenv(find_dotenv())
    return OpenAI(
        base_url="http://localhost:11434/v1",
        api_key=os.environ["OLLAMA_API_KEY"],
    )

if __name__ == "__main__":
    # Smoke test — run `uv run python src/client.py` to verify the default
    # chat client (make_chat_client) is wired correctly.
    response = make_chat_client().chat.completions.create(
        model="kimi-k3",
        messages=[
            {"role": "user", "content": "Write a short poem about the color blue"}
        ],
    )
    print(response.choices[0].message.content)
