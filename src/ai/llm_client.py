from __future__ import annotations

from src.config import settings

_client = None


def get_groq_client():
    global _client

    if _client is None:
        if not settings.groq_api_key:
            raise RuntimeError("GROQ_API_KEY is missing. Set it in .env or environment variables.")
        try:
            from groq import Groq
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "groq package is not installed. Install requirements.txt or use mock mode."
            ) from exc
        _client = Groq(api_key=settings.groq_api_key)

    return _client
