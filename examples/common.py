"""Gemeinsame Konfiguration: lädt .env und stellt Client und Modell bereit."""

import os
import sys

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
