"""Testdaten generieren."""

import json
from pathlib import Path

from common import add_user_message, chat


def generate_dataset():
    prompt = """
Generate an evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects, each representing task that requires Python, JSON, or a Regex to complete.

Example output:
```json
[
  {
    "task": "Description of task",
  },
  ...additional
]
```

* Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a single regex
* Focus on tasks that do not require writing much code

Please generate 3 objects.
"""

    messages = []
    add_user_message(messages, prompt)
    # Structured Outputs statt Prefill/Stop-Sequenzen: die API garantiert
    # Antworten, die dem Schema entsprechen (Wurzel muss ein Objekt sein).
    output_config = {
        "format": {
            "type": "json_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "tasks": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {"task": {"type": "string"}},
                            "required": ["task"],
                            "additionalProperties": False,
                        },
                    }
                },
                "required": ["tasks"],
                "additionalProperties": False,
            },
        }
    }
    text = chat(messages, output_config=output_config)
    return json.loads(text)["tasks"]


dataset = generate_dataset()
print(dataset)

DATASET_PATH = Path(__file__).parent / "dataset.json"

with open(DATASET_PATH, "w") as f:
    json.dump(dataset, f, indent=2)
