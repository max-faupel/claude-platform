"""Einfacher Messages-Aufruf."""

from common import MODEL, get_client

client = get_client()

response = client.messages.create(
    model=MODEL,
    max_tokens=1024,
    messages=[{"role": "user", "content": "Erkläre in zwei Sätzen, was ein LLM ist."}],
)

for block in response.content:
    if block.type == "text":
        print(block.text)

print(f"\nTokens: {response.usage.input_tokens} in / {response.usage.output_tokens} out")
