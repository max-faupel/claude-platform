"""System-Prompt und Multi-Turn-Konversation (die API ist zustandslos)."""

from common import MODEL, get_client

client = get_client()

SYSTEM = "Du bist ein Python-Tutor. Antworte knapp und gib immer ein kurzes Codebeispiel."

messages = [{"role": "user", "content": "Wie lese ich eine JSON-Datei?"}]

for follow_up in [None, "Und wie schreibe ich sie wieder?"]:
    if follow_up:
        messages.append({"role": "user", "content": follow_up})
    response = client.messages.create(
        model=MODEL, max_tokens=1024, system=SYSTEM, messages=messages
    )
    text = "".join(b.text for b in response.content if b.type == "text")
    print(f"Claude: {text}\n")
    # Antwort in den Verlauf aufnehmen, damit der nächste Turn Kontext hat
    messages.append({"role": "assistant", "content": response.content})
