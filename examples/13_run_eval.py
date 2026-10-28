"""Eval ausführen."""

import json
from pathlib import Path
from statistics import mean

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

def grade_by_model(test_case, solution):
    # Erstelle Bewertungsprompt
    eval_prompt = f"""
You are an expert code reviewer. Evaluate this AI-generated solution.

<task>
{test_case["task"]}
</task>
<solution>
{solution}
</solution>

Provide your evaluation as a structured JSON object with:
- "strengths": An array of 1-3 key strengths
- "weaknesses": An array of 1-3 key areas for improvement
- "reasoning": A concise explanation of your assessment
- "score": A number between 1-10
"""

    print(f"Eval prompt: {eval_prompt}")

    messages = []
    add_user_message(messages, eval_prompt)
    output_config = {
        "format": {
            "type": "json_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "strengths": {"type": "array", "items": {"type": "string"}},
                    "weaknesses": {"type": "array", "items": {"type": "string"}},
                    "reasoning": {"type": "string"},
                    "score": {"type": "integer"},
                },
                "required": ["strengths", "weaknesses", "reasoning", "score"],
                "additionalProperties": False,
            },
        }
    }

    eval_text = chat(messages, output_config=output_config)
    return json.loads(eval_text)


def run_test_case(test_case):
    """Ruft run_prompt auf und bewertet anschließend das Ergebnis."""
    output = run_prompt(test_case)
    model_grade = grade_by_model(test_case, output)

    score = model_grade["score"]
    reasoning = model_grade["reasoning"]

    return {"output": output, "test_case": test_case, "score": score, "reasoning": reasoning}


def run_eval(dataset):
    """Führt run_test_case für jeden Testfall des übergebenen Datensatzes aus."""
    results = []

    for test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)

    average_score = mean(result["score"] for result in results)
    print(f"Average score: {average_score}")

    return results

DATASET_PATH = Path(__file__).parent / "dataset.json"

with open(DATASET_PATH) as f:
    dataset = json.load(f)

results = run_eval(dataset)
# print(json.dumps(results, indent=2))
