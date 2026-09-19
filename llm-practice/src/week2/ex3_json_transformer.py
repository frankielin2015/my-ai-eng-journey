"""Week 2 deliverable 3 — JSON transformer (function calling).

Take messy, unstructured input and use function calling to produce clean,
validated JSON output. This is the "real world" version of ex1 — instead of
fake weather data, you transform actual messy text into structured records.

Scenario: You receive raw text snippets from a legacy system. Each snippet
contains a person record with inconsistent formatting. Use function calling
to normalize them into a consistent PersonRecord schema.

Run with:

    uv run python src/week2/ex3_json_transformer.py

Expected behavior:
  - Each raw snippet triggers 1+ function calls to normalize fields
  - Final output is a validated PersonRecord JSON object
  - Invalid inputs (missing name, etc.) are caught and reported
"""
from __future__ import annotations

import json
import os
from typing import Literal

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError

load_dotenv()

client = OpenAI(
    base_url="https://ollama.com/v1",
    api_key=os.environ["OLLAMA_API_KEY"],
)

MODEL = "deepseek-v4-flash:cloud"


# ---------------------------------------------------------------------------
# TODO 1: Define the output schema.
#
# PersonRecord with:
#   - name: str (required)
#   - email: str | None (optional — may be missing in source)
#   - phone: str | None (optional)
#   - tags: list[str], max 3 items — e.g. ["customer", "vip", "churned"]
#   - source: Literal["legacy_crm", "web_form", "api_import", "unknown"]
#
# Hint: optional fields in Pydantic v2 use `str | None = None` or
#       `Field(default=None)`. Literal for enums.
# ---------------------------------------------------------------------------
class PersonRecord(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None
    tags: list[str] = Field(default_factory=list, max_length=3)
    source: Literal["legacy_crm", "web_form", "api_import", "unknown"] = "unknown"


# ---------------------------------------------------------------------------
# TODO 2: Define the tool schema.
#
# One function: normalize_person
#   - description: "Normalize a raw person record into structured fields"
#   - parameters: JSON Schema matching PersonRecord fields, plus:
#       * source: infer from context clues in the raw text
#       * all fields optional in the tool schema (model infers what it can)
#         except 'name' which is required
#
# The tool schema is what you pass to OpenAI — use the same pattern as ex1.
# ---------------------------------------------------------------------------
tools = [{
    "type": "function",
    "function": {
        "name": "normalize_person",
        "description": "Normalize a raw person record into structured fields",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string"},
                "phone": {"type": "string"},
                "tags": {"type": "array", "items": {"type": "string"}},
                "source": {"type": "string", "enum": ["legacy_crm", "web_form", "api_import", "unknown"]}
            },
            "required": ["name"]
        }
    }
}]


# ---------------------------------------------------------------------------
# TODO 3: Implement the transformer function.
#
# def transform_person(raw_text: str) -> PersonRecord | None:
#
# Steps:
#   1. Call client.chat.completions.create with tools=[TOOL_SCHEMA]
#   2. Check tool_calls — if none, return None (model didn't call the function)
#   3. Extract arguments JSON from tool_calls[0].function.arguments
#   4. Validate into PersonRecord (use model_validate, not model_validate_json
#      since arguments is already a dict string)
#   5. Return the PersonRecord
#
# On ValidationError, log and return None.
# On missing tool_calls, return None.
# ---------------------------------------------------------------------------
def transform_person(raw_text: str) -> PersonRecord | None:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a data normalization assistant."},
            {"role": "user", "content": raw_text},
        ],
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "normalize_person"}},
    )
    tool_calls = response.choices[0].message.tool_calls if response.choices[0].message.tool_calls else None
    args = json.loads(tool_calls[0].function.arguments) if tool_calls else None

    try:
        record = PersonRecord.model_validate(args)
        return record
    except ValidationError as e:
        print(f"  → validation error: {e}")
        return None
    

# ---------------------------------------------------------------------------
# Test data — messy, inconsistent, realistic legacy snippets.
# ---------------------------------------------------------------------------
RAW_SNIPPETS = [
    # happy path: clear, complete
    "John Smith, john.smith@example.com, 555-123-4567. VIP customer, high value. Source: legacy CRM import.",

    # missing email, has phone
    "Sarah Johnson — no email on file. Call her at (555) 987-6543. Tagged: churned-risk. From web form.",

    # missing phone, weird formatting
    "mike.chen@company.io | Mike Chen | imported via API | tags: new-signup, beta-tester",

    # minimal info — name only
    "Unknown contact from trade show. Name: Alex. No other details.",

    # ambiguous source
    "Jennifer Walsh, jwalsh@email.com. Met at conference. Seems interested.",
]


# ---------------------------------------------------------------------------
# TODO 4: main() — run all snippets, print results.
#
# For each snippet:
#   - print the raw input
#   - call transform_person()
#   - if result is None, print "→ failed to transform"
#   - if result is PersonRecord, print fields
#   - if ValidationError inside transform_person was caught, it returns None
#
# At the end, print a summary: N succeeded, M failed.
# ---------------------------------------------------------------------------
def main() -> None:
    for i, text in enumerate(RAW_SNIPPETS):
        print(f"\n=== Case {i}: {text[:60]!r}{'...' if len(text) > 60 else ''}")
        try:
            result = transform_person(text)
        except ValidationError as exc:
            print(f"  → validation error: {exc}")
            result = None
        if result is None:
            print("  → failed to transform")
        else:
            print(f"  → transformed: {result.model_dump_json(indent=2)}")


if __name__ == "__main__":
    main()
