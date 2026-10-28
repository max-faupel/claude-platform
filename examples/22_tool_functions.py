"""Tool Use: manueller Ablauf mit einem eigenen Tool (aktuelle Uhrzeit)."""

from datetime import datetime

from anthropic.types import ToolParam

from common import MODEL, add_assistant_message, add_user_message, chat, get_client

client = get_client()


def get_current_datetime(date_format="%Y-%m-%d %H:%M:%S"):
    if not date_format:
        raise ValueError("date_format darf nicht leer sein")
    return datetime.now().strftime(date_format)


get_current_datetime_schema = ToolParam({
    "name": "get_current_datetime",
    "description": "Returns the current date and time formatted according to the specified format",
    "input_schema": {
        "type": "object",
        "properties": {
            "date_format": {
                "type": "string",
                "description": "A string specifying the format of the returned datetime. Uses Python's strftime format codes.",
                "default": "%Y-%m-%d %H:%M:%S"
            }
        },
        "required": []
    }
})

tools = [get_current_datetime_schema]

messages = []

add_user_message(messages, "Wie spät ist es genau? Bitte im Format HH:MM:SS.")

response = client.messages.create(
    model=MODEL,
    max_tokens=4000,
    messages=messages,
    tools=tools,
)

print(f"Antwort: {response.content}")

add_assistant_message(messages, response.content)

if response.stop_reason == "tool_use":
    tool_results = []
    for block in response.content:
        if block.type != "tool_use":
            continue
        try:
            result = get_current_datetime(**block.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result,
            })
        except Exception as e:
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": f"Fehler: {e}",
                "is_error": True,
            })

    add_user_message(messages, tool_results)

    output = chat(messages, tools=tools)
    print(f"Ausgabe: {output}")
else:
    print(f"Kein Tool-Aufruf (stop_reason: {response.stop_reason})")
