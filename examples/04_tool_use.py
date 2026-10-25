"""Tool Use: Der Tool Runner führt die Schleife aus Anfrage -> Tool -> Ergebnis automatisch."""

from anthropic import beta_tool
from common import MODEL, get_client

client = get_client()


@beta_tool
def get_weather(location: str, unit: str = "celsius") -> str:
    """Aktuelles Wetter für einen Ort abrufen.

    Args:
        location: Stadt, z. B. "Berlin".
        unit: Temperatureinheit, "celsius" oder "fahrenheit".
    """
    # Stub: hier würde ein echter Wetterdienst abgefragt
    return f"18 Grad {unit}, leicht bewölkt in {location}"


runner = client.beta.messages.tool_runner(
    model=MODEL,
    max_tokens=2048,
    tools=[get_weather],
    messages=[{"role": "user", "content": "Wie ist das Wetter in Berlin und in München?"}],
)

final = None
for message in runner:
    final = message

print("".join(b.text for b in final.content if b.type == "text"))
