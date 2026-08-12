"""
Thin client for the LLM Router running on the Mac mini (192.168.1.53:8080).
Returns None on any failure so callers can fall back to rule-based output.
"""
from __future__ import annotations

import logging

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)

_TIMEOUT = 120  # seconds — Ollama on Pi 2 can be slow


def chat(
    query: str,
    *,
    backend: str = "auto",
    system: str = "",
    rag_enabled: bool = True,
    context_k: int = 5,
    private: bool = False,
) -> str | None:
    """
    Call POST /chat on the LLM Router. Returns the response string,
    or None if the router is unreachable or returns an error.
    """
    try:
        payload = {
            "query": query,
            "backend": backend,
            "system": system,
            "rag_enabled": rag_enabled,
            "context_k": context_k,
            "private": private,
        }
        resp = httpx.post(
            f"{settings.LLM_ROUTER_URL}/chat",
            json=payload,
            timeout=_TIMEOUT,
        )
        resp.raise_for_status()
        return resp.json().get("response")
    except Exception as exc:
        logger.warning("LLM Router unavailable (%s) — using fallback", exc)
        return None
