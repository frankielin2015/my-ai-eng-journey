"""Week 2 deliverable 4 — support ticket classifier (function calling).

Classify incoming support tickets into categories using function calling,
then route them to the appropriate handler. This combines structured output
with decision-making — the model picks a category AND a priority.

Scenario: You're building the intake system for a support team. Tickets come
in as free text. Your classifier must:
  1. Pick a category: bug_report | feature_request | billing | account | other
  2. Pick a priority: low | medium | high | critical
  3. Extract a one-sentence summary
  4. Suggest which team should handle it

Run with:

    uv run python src/week2/ex4_classifier.py

Expected behavior:
  - Each ticket triggers exactly one classify_ticket call
  - Output is a validated TicketClassification
  - Routing decision printed for each ticket
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

MODEL = "kimi-k3:cloud"


# ---------------------------------------------------------------------------
# TODO 1: Define the classification schema.
#
# TicketClassification with:
#   - category: Literal["bug_report", "feature_request", "billing", "account", "other"]
#   - priority: Literal["low", "medium", "high", "critical"]
#   - summary: str (one sentence, max 100 chars — use Field(max_length=100))
#   - suggested_team: Literal["engineering", "product", "billing", "support"]
#
# All fields required.
# ---------------------------------------------------------------------------
class TicketClassification(BaseModel):
    category: Literal["bug_report", "feature_request", "billing", "account", "other"]
    priority: Literal["low", "medium", "high", "critical"]
    summary: str = Field(..., max_length=100)
    suggested_team: Literal["engineering", "product", "billing", "support"]


# ---------------------------------------------------------------------------
# TODO 2: Define the tool schema.
#
# Function: classify_ticket
#   - description: "Classify a support ticket by category, priority, and routing"
#   - parameters: JSON Schema matching TicketClassification
#
# Same pattern as ex1 and ex3.
# ---------------------------------------------------------------------------
TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "classify_ticket",
        "description": "Classify a support ticket by category, priority, and routing",
        "parameters": TicketClassification.model_json_schema()
    }
}

# ---------------------------------------------------------------------------
# TODO 3: Implement the classifier.
#
# def classify_ticket(ticket_text: str) -> TicketClassification | None:
#
# Same structure as ex3:
#   1. create() with tools
#   2. extract tool_calls
#   3. parse arguments
#   4. validate into TicketClassification
#   5. return or None on failure
#
# Add one twist: if category is "other" AND priority is "critical",
# print a warning — something is misclassified or the ticket is unclear.
# ---------------------------------------------------------------------------
def classify_ticket(ticket_text: str, max_retries: int = 2) -> TicketClassification | None:
    for attempt in range(max_retries + 1):
        # Prompt constraint prevents common failures; retry is safety net
        system_msg = "You are a support ticket classification assistant. Keep summary under 100 characters."
        if attempt > 0:
            system_msg += " This is a retry — strictly enforce the 100-character limit."

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": ticket_text},
            ],
            tools=[TOOL_SCHEMA],
            tool_choice={"type": "function", "function": {"name": "classify_ticket"}},
        )

        tool_calls = response.choices[0].message.tool_calls
        if not tool_calls:
            print(f"  → attempt {attempt}: model did not call the function")
            if attempt == max_retries:
                return None
            continue

        args = json.loads(tool_calls[0].function.arguments)

        try:
            classification = TicketClassification.model_validate(args)
            if attempt > 0:
                print(f"  → succeeded on retry {attempt}")
            return classification
        except ValidationError as e:
            print(f"  → attempt {attempt}: validation error: {e.errors()[0]['msg']}")
            if attempt == max_retries:
                print(f"  → max retries ({max_retries}) exceeded")
                return None

    return None


# ---------------------------------------------------------------------------
# TODO 4: Implement the router.
#
# def route_ticket(classification: TicketClassification) -> str:
#
# Pure function — no LLM call. Given a classification, return the team name.
#
# Routing rules:
#   - category "bug_report" → "engineering"
#   - category "feature_request" → "product"
#   - category "billing" → "billing"
#   - category "account" → "support"
#   - category "other" + priority "critical" → "support" (escalation)
#   - category "other" otherwise → "support" (triage)
#
# Return just the team string.
# ---------------------------------------------------------------------------
def route_ticket(classification: TicketClassification) -> str:
    if classification.category == "bug_report":
        return "engineering"
    elif classification.category == "feature_request":
        return "product"
    elif classification.category == "billing":
        return "billing"
    elif classification.category == "account":
        return "support"
    elif classification.category == "other":
        if classification.priority == "critical":
            return "support"  # escalation
        else:
            return "support"  # triage
    else:
        raise ValueError(f"Unknown category: {classification.category}")


# ---------------------------------------------------------------------------
# Test tickets — realistic support tickets with varying clarity.
# ---------------------------------------------------------------------------
TICKETS = [
    # happy path: clear bug
    "The export button crashes when I click it. Console shows TypeError: Cannot read property 'map' of undefined.",

    # billing issue
    "I was charged twice for my subscription this month. Order #12345 and #12346. Please refund one.",

    # feature request
    "Would love to see dark mode support. My eyes hurt after long sessions.",

    # account issue
    "Can't log in. Reset password email never arrives. Checked spam folder.",

    # unclear / ambiguous
    "It doesn't work right. Please fix.",

    # critical bug
    "DATA LOSS: All my saved projects disappeared after the latest update. This is unacceptable.",
]


# ---------------------------------------------------------------------------
# TODO 5: main() — classify + route all tickets.
#
# For each ticket:
#   - print ticket text (truncated to 60 chars)
#   - call classify_ticket()
#   - if None, print "→ failed to classify"
#   - if TicketClassification:
#       * print category, priority, summary
#       * call route_ticket() and print the team
#       * if category == "other" and priority == "critical", print warning
#
# At the end, print summary counts by category and by priority.
# ---------------------------------------------------------------------------
def main() -> None:
    for i, text in enumerate(TICKETS):
        print(f"\n=== Ticket {i}: {text[:60]!r}{'...' if len(text) > 60 else ''}")
        classification = classify_ticket(text)
        if classification is None:
            print("  → failed to classify")
            continue

        print(f"  → category: {classification.category}")
        print(f"  → priority: {classification.priority}")
        print(f"  → summary: {classification.summary}")

        team = route_ticket(classification)
        print(f"  → suggested team: {team}")

        if classification.category == "other" and classification.priority == "critical":
            print("  → WARNING: 'other' category with 'critical' priority — check ticket!")


if __name__ == "__main__":
    main()
