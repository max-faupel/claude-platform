# Claude Platform Training – Python-Beispiele

Experimentierprojekt für die Python-Beispiele des Claude-Platform-Trainings (Anthropic SDK).

## Befehle
- `uv sync` – Abhängigkeiten installieren (.venv)
- `uv run python examples/01_messages.py` – Beispiel ausführen (analog 02–04)
- `uv add <paket>` – Abhängigkeit hinzufügen (nie `pip install`)

## Konfiguration
Alles über `.env` im Projektroot (Vorlage: `.env.example`):
- `ANTHROPIC_BASE_URL` – API-Endpunkt (auch Gateways/Proxys)
- `ANTHROPIC_API_KEY` – API-Key (Secret, nie committen oder ausgeben)
- `ANTHROPIC_MODEL` – Modell-ID, z. B. `claude-sonnet-5-5`

## Struktur
- `examples/common.py` – lädt `.env`, liefert `get_client()` und `MODEL`
- `examples/01_messages.py` – einfacher Aufruf
- `examples/02_system_multiturn.py` – System-Prompt, Multi-Turn
- `examples/03_streaming.py` – Streaming
- `examples/04_tool_use.py` – Tool Use mit Tool Runner (`@beta_tool`)

## Konventionen
- Projektmanagement ausschließlich mit uv; Python >= 3.12.
- Client nur über `common.get_client()`, Modell nur über `common.MODEL` – keine hartkodierten Werte.
- Neue Beispiele als `examples/NN_name.py`, selbstständig lauffähig, mit `from common import ...`.
- Kommentare und Ausgaben auf Deutsch.
- Kein `temperature`/`top_p`/`top_k` und kein `budget_tokens` bei aktuellen Claude-Modellen (führt zu 400).
