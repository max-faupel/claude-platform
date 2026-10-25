"""Eval ausführen."""

import json
from pathlib import Path

from common import add_user_message, chat


def run_prompt(test_case):
    """Kombiniert den Prompt mit der Aufgabe des Testfalls und gibt die Antwort zurück."""
    prompt = f"""
Please solve the following task:

{test_case["task"]}
"""

    messages = []
    add_user_message(messages, prompt)
    output = chat(messages)
    return output


def run_test_case(test_case):
    """Ruft run_prompt auf und bewertet anschließend das Ergebnis."""
    output = run_prompt(test_case)

    # TODO - Bewertung
    score = 10

    return {"output": output, "test_case": test_case, "score": score}


def run_eval(dataset):
    """Führt run_test_case für jeden Testfall des übergebenen Datensatzes aus."""
    results = []

    for test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)

    return results


DATASET_PATH = Path(__file__).parent / "dataset.json"

with open(DATASET_PATH) as f:
    dataset = json.load(f)

results = run_eval(dataset)
print(json.dumps(results, indent=2))
