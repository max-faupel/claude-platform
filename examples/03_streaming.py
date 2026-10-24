"""Streaming: Text erscheint, sobald er generiert wird."""

from common import MODEL, get_client

client = get_client()

with client.messages.stream(
    model=MODEL,
    max_tokens=2048,
    messages=[{"role": "user", "content": "Schreibe ein kurzes Gedicht über Python."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
    final = stream.get_final_message()

print(f"\n\nStop-Reason: {final.stop_reason}")
