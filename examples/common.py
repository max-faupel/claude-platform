"""Gemeinsame Konfiguration: lädt .env und stellt Client und Modell bereit."""

import os
import sys
from functools import cache

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


def _require(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        sys.exit(f"Fehlende Einstellung {name} - bitte in .env eintragen (siehe .env.example).")
    return value


MODEL = _require("ANTHROPIC_MODEL")


def get_client() -> Anthropic:
    return Anthropic(
        base_url=_require("ANTHROPIC_BASE_URL"),
        api_key=_require("ANTHROPIC_API_KEY"),
    )


def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})


def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})


@cache
def _client() -> Anthropic:
    return get_client()


def chat(messages, system=None, stop_sequences=None, output_config=None, tools=None):
    """Einfacher Aufruf; gibt den Text der Antwort zurück."""
    params = {
        "model": MODEL,
        "max_tokens": 1000,
        "messages": messages,
    }
    if system:
        params["system"] = system
    if tools:
        params["tools"] = tools
    if stop_sequences:
        params["stop_sequences"] = stop_sequences
    if output_config:
        params["output_config"] = output_config

    response = _client().messages.create(**params)
    return next(b.text for b in response.content if b.type == "text")
