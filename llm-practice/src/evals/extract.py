"""Week 6 — Extractor: the system under test.

Turns a short meeting note into action items. This is the FIRST LLM
call in the eval pipeline; judge.py (the SECOND call) grades its
output, and run_eval.py sequences both across ready_tests().

CONTRACT
    extract_action_items(text) -> list[dict]
    each dict: {"action": str, "owner": str|None, "due_date": str|None}
    Empty list means "nothing to extract" — run_eval.py's hardened
    bridge fallback handles that case (run_eval.py § Step 3).

DECISIONS
- Model: deepseek-v4.1-flash — cheaper than kimi-k2/kimi-k3. Same
  model grades its own output downstream (self-preference bias is
  documented in run_eval.py's DECISIONS block).
- temperature=0: eval numbers must be reproducible. With sampling
  noise, a prompt change cannot be told apart from randomness —
  which would undercut the README's "what we changed" story.
  (Matches judge.py's determinism.)
- Prompted JSON is a request, not a constraint: the model can return
  prose, fences, or extra fields at any time. That's why the fence
  strip + json.loads() pattern exists — and why judge.py wraps its
  whole body in try/except while this file deliberately does NOT
  (judge.py owns the never-raise contract; different failure surfaces
  stay visible: extract raises → run_eval makes an extract-error row).
- Hand-rolled on purpose (no LangChain, no structured-output lib):
  the failure modes ARE the curriculum.

────────────────────────────────────────────────────────────────────────

## WHEN YOU GET STUCK

- 401 / API key errors → check OPENCODE_API_KEY is set in .env
  (client.py finds it via find_dotenv()).
- json.JSONDecodeError → the model returned prose, not a JSON list.
  Inspect `content` in the __main__ debugger below.
- KeyError on `action` / `owner` / `due_date` → the LLM returned
  different keys. The user prompt names the exact schema — check it
  wasn't paraphrased.
- ModuleNotFoundError: No module named 'client' → run from inside
  src/ so the path shim below resolves sibling imports.

## EVAL OF THE EVAL

If an extracted row looks wrong on a golden test, do FAILURE TRIAGE
(golden_dataset.py header) BEFORE editing this prompt:
    1. TEST WRONG   2. TEST TOO STRICT   3. SYSTEM BROKEN
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
    """Extract action items from one meeting note (the system under test).

    Args:
        text: A meeting notes snippet (one of golden_dataset's `input`).

    Returns:
        A list of action items, each shaped:
            {"action": str, "owner": str|None, "due_date": str|None}
        Empty list means "nothing to extract" (matches test-004).

    Raises:
        json.JSONDecodeError / KeyError: if the LLM returns prose or
        an unexpected shape. run_eval.py § Step 3 wraps this call so
        an exception becomes an "extract-error:" row instead of
        killing the run.
    """
    response = make_chat_client().chat.completions.create(
        model="deepseek-v4.1-flash",
        temperature=0,  # determinism: eval numbers must be reproducible
        messages=[
            {"role": "system",
             "content": ("You are a meeting notes extractor, you are "
                         "expert at extract meeting notes and you are "
                         "known for precision and correctness")},
            {"role": "user",
             "content": (f"extract action items from this meeting note: {text}; "
                         "Return a JSON list of dicts with keys: action, "
                         "owner, due_date. Use null for fields that don't "
                         "apply.")},
        ],
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
