"""Week 6 — Stub extractor.

This is the "system under test" for golden_dataset.py. It exists so
judge.py can run end-to-end. Replace the stub with a real prompt once
you've verified the dataset shape.

────────────────────────────────────────────────────────────────────────

Step 1 — Read the signature  (verb: read)

  do:   Note that extract_action_items(text) -> list[dict]
        Each dict MUST have this shape (matching golden_dataset.py):
          {"action": str, "owner": str|None, "due_date": str|None}
        judge.py compares dict-to-dict — mismatched keys = wrong scores.
  done: you know what shape judge.py will consume.

────────────────────────────────────────────────────────────────────────

Step 2 — Make it return SOMETHING  (verb: edit)

  do:   In the function body at the bottom of this file, look for the
        `# TODO Step 2:` marker (right above `return []`). Replace the
        line below it with a non-empty stub:
          return [{"action": text, "owner": None, "due_date": None}]
        (this is wrong but runnable — judge.py will see all 3 fields
        and the field-level score will be predictable)
  done: `python -c "from evals.extract import extract_action_items;
                   print(extract_action_items('test'))"` prints a
        non-empty list with one dict.

────────────────────────────────────────────────────────────────────────

Step 3 — Make it RIGHT  (verb: write)

  do:   In the SAME place (where Step 2's stub is), replace the stub
        with a real LLM call. The API pattern from src/client.py:83-89:
          client = make_chat_client()
          prompt = (
            f"Extract action items from this meeting note.\n"
            f"Return a JSON list of dicts with keys: "
            f"action, owner, due_date.\n"
            f"Use null for fields that don't apply.\n\n"
            f"Note: {text}"
          )
          response = client.chat.completions.create(
            model="kimi-k3",  # see src/client.py:43 for other models
            messages=[{"role": "user", "content": prompt}],
          )
          content = response.choices[0].message.content
          # Strip ```json ... ``` fences, then json.loads() -> list[dict]
          return parsed_list
  done: output matches the `expected` shape for at least one row in
        golden_dataset (run judge.py to verify).

────────────────────────────────────────────────────────────────────────

## WHERE to write the code

All edits happen INSIDE `extract_action_items()` at the very bottom of
this file. Look for the two TODO markers right above `return []`:
    # TODO Step 2: ...
    # TODO Step 3: ...
Step 2 replaces the `return []` line. Step 3 replaces Step 2's line
with the LLM call template from the docstring above.

────────────────────────────────────────────────────────────────────────

## WHEN YOU GET STUCK

- `ModuleNotFoundError: No module named 'client'` → path shim below
  isn't running. Run from inside `src/`.
- judge.py says "no items found" → stub still returns []. Run Step 2.
- JSON parse errors → LLM returned prose, not JSON. Strip markdown
  fences (```json ... ```) before json.loads().
- KeyError on `action` / `owner` / `due_date` → prompt returned
  different keys. Re-read Step 1's schema.
- 401 / API key errors → check OPENCODE_API_KEY is set in .env.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# Repo convention: see week5/query.py:30 and week5/benchmark.py:39
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from client import make_chat_client


def extract_action_items(text: str) -> list[dict]:
    """Stub extractor — returns []. Replace per Steps 2-3.

    Args:
        text: A meeting notes snippet (one of golden_dataset's `input`).

    Returns:
        A list of action items, each shaped:
            {"action": str, "owner": str|None, "due_date": str|None}
        Empty list means "nothing to extract" (matches test-004).

    Schema MUST match golden_dataset.py's `expected`:
        {"action": "...", "owner": "...", "due_date": "..."}
    """
    # TODO Step 2: replace the `return []` line below with a non-empty stub
    #   matching the schema above. Suggested stub:
    #     return [{"action": text, "owner": None, "due_date": None}]
    # TODO Step 3: replace that stub with the LLM call template from
    #   the docstring § Step 3 (uses make_chat_client + chat.completions.create)
    response = make_chat_client().chat.completions.create(
        model= "deepseek-v4.1-flash",
        messages=[
             {"role": "system", "content": "You are a meeting notes extractor, you are expert at extract meeting notes and you are known for precision and correctness"},
             {"role": "user", "content": f"""extract action items from this meeting note: {text}; 
             Return a JSON list of dicts with keys: action, owner, due_date. Use null for fields that don't apply."""}
              ]
    )
    content = response.choices[0].message.content
    cleaned = re.sub(r"\`\`\`(?:json)?", "", content).strip()
    items = json.loads(cleaned)
    return items


if __name__ == "__main__":
    # Debug entry point. Set breakpoints inside extract_action_items above
    # to inspect: prompt, response, content, cleaned, items.
    #
    # VS Code: open this file, click in the gutter to set a breakpoint,
    # then press F5 (or Run > Start Debugging).
    test_note = "John to send the spec by Friday."
    result = extract_action_items(test_note)
    print(result)
