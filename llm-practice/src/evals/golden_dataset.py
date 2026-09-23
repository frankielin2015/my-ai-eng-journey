"""Golden dataset for the meeting notes extraction task (Week 6, Exercise A).

## PATH — do these in order. Each step has a "done" signal.

────────────────────────────────────────────────────────────────────────

Step 0 — Can you run this file?  (verb: run)

  do:   cd /Users/xiaofalin/WorkSpace/my-ai-eng-journey/llm-practice/src
        uv run python -m evals.golden_dataset
  done: prints "ready: 2/5 tests ready (2 exemplars + 3 TODO)"
        If the import fails, your environment is broken — fix that first.

────────────────────────────────────────────────────────────────────────

Step 1 — Read the schema  (verb: read)

  do:   Read the field list below. Each entry in GOLDEN_DATASET is a dict:
          - id             stable identifier (test-001, test-002, ...)
          - dimension      which axis this test probes (auditable coverage)
          - input          the meeting notes text the system will see
          - expected       the {action, owner, due_date} dict the system
                           should produce
          - added_because  why this test exists (becomes README story)
          - provenance     "exemplar" (shipped) or "user" (you wrote it)
          - _target_dimensions  (TODO rows only) — the candidate axes
  done: you can name what each field is FOR, not just its type.

────────────────────────────────────────────────────────────────────────

Step 1.5 — Stub `extract.py`  (verb: write)

  do:   Open `evals/extract.py` (the file the docstring has been
        referencing). It currently returns []. Follow its Steps 1-3 to
        make it return something runnable.
  done: `python -c "from evals.extract import extract_action_items;
                   print(extract_action_items('test note'))"` prints
        a non-empty list of dicts.

  Why this step is here: the system under test must exist before you
  can grade against it. The plan's success test (line 230) explicitly
  says the judge "grades outputs from a cheaper model."

────────────────────────────────────────────────────────────────────────

Step 2 — Look at the 2 finished rows  (verb: read)

  do:   Scroll to test-001 and test-004 at the bottom of this file.
  done: you can articulate why these two are different.
        Hint: test-001 has values; test-004 has None for everything.

────────────────────────────────────────────────────────────────────────

Step 3 — Run the ready check  (verb: call)

  do:   uv run python -c "from evals.golden_dataset import ready_tests;
                          print(len(ready_tests()))"
  done: prints 2 (the count is computed by filtering TODO rows out —
        not hardcoded, no docstring/code drift).

────────────────────────────────────────────────────────────────────────

Step 4 — Write test-002  (verb: write)

  do:   Fill in test-002 with the prescribed dimension "implicit_owner".
          - input:    paste 2-3 sentences from a real meeting note
                      (your calendar, Slack, or a transcript)
          - expected: {action, owner, due_date} per SCORING_CONTRACT
          - delete the _target_dimensions key
          - set provenance to "user"
  done: ready_tests() returns 3.

  THEORY (C1 — bounded evidence): this row confirms that the system can
  extract an action when the owner is implied (not named). Write ONE
  comment above the row answering: "What failure mode does this row
  NOT rule out?" If you cannot name one, the row is redundant with 001/004.

────────────────────────────────────────────────────────────────────────

Step 5 — Diagnose a broken row  (verb: read + answer)

  do:   The FAILURE TRIAGE block below lists 3 failure modes. For each,
        name which `_target_dimensions` value would catch it.
  done: you have a 3-row table mapping failure-mode → dimension.

  THEORY (C4 — iterate the eval): when a test fails, the FAILURE TRIAGE
  order matters. System-broken is the LAST diagnosis, not the first.

────────────────────────────────────────────────────────────────────────

Step 6 — Write test-003 and test-005  (verb: write)

  do:   - test-003: dimension="past_tense_done"  (already done, NOT an action)
        - test-005: dimension="discussion_not_action"  (discussed, not assigned)
        Fill input/expected, set provenance="user", delete _target_dimensions.
  done: ready_tests() returns 5; each row has a distinct dimension.

────────────────────────────────────────────────────────────────────────

Step 7 — Decide the scoring rubric  (verb: decide)

  do:   SCORING_CONTRACT (below) defines 4 policies as STRINGS.
        Turn each into a 0/1/2 score with a one-line justification in
        JUDGE_RUBRIC. Example for none_policy:
          "For each field: if expected is null, score 1 iff the model's
           value is null, empty, or explicitly states absence. Score 0
           if the model invented a value."
  done: every policy has {0: ..., 1: ..., 2: ...} in JUDGE_RUBRIC.

  THEORY (C2 — source from reality): your rubric scores what a real user
  would notice, not what's easy to count.

────────────────────────────────────────────────────────────────────────

Step 8 — Grow to 15-20 pairs  (verb: plan)

  do:   Append test-006..test-015 below. Each new row needs a `dimension`
        that is NOT already used. Source from real notes (your own,
        not invented). One dimension per row.
  done: ready_tests() returns ≥15; coverage matrix shows ≥6 distinct
        dimensions.

  THEORY (C5 — incremental build): at n=5, one failure is 20 points —
  you cannot interpret scores yet. After your first scored run, delete
  one passing row and rerun. Watch the score move 20 points. That
  feeling is why n≥15.

────────────────────────────────────────────────────────────────────────

## WHAT THIS IS NOT

This is not a finished dataset. It is 2 examples + 3 scaffolds for you.
"The system" is `evals/extract.py` — a stub you wired up in Step 1.5.

## WHEN YOU GET STUCK

- ready_tests() returns less than you expect → a row has a None value
- judge.py crashes → your SCORING_CONTRACT keys don't match the rubric
- the rubric feels arbitrary → that's C2. Score what the USER would notice.

## FAILURE TRIAGE (when a test fails)

1. TEST WRONG. Is `expected` actually correct? If not, fix it and log why
   in `added_because`. Rerun.
2. TEST TOO STRICT. Is the system output semantically equal but textually
   different? If so, loosen `expected` OR note this as a known ambiguity.
3. SYSTEM BROKEN. Only after 1 and 2 are ruled out. Fix the prompt,
   model, or pipeline.

Do NOT change the prompt before ruling out 1 and 2.

## SCORING CONTRACT

Defines what "correct" means for the judge (judge.py reads this):

  - matching:           "semantic_per_field"  (LLM-as-judge scores each field)
  - none_policy:        "None" means "field absent", distinct from ""
  - date_canonicalize:  relative dates (e.g. "Friday", "next Tuesday") are
                        evaluated as their STRING form. If you ever
                        canonicalize to ISO, you MUST freeze a reference
                        date — otherwise "next Tuesday" passes on Tuesday
                        and fails on Wednesday.
  - case_policy:        owners are case-preserving as written ("Team"
                        stays "Team"); do not normalize.

If you change this, judge.py and any past scores are no longer comparable.
"""

import sys
from pathlib import Path

# Repo convention: every module under src/ needs this shim to find sibling
# packages. See `week5/query.py:30` and `week5/benchmark.py:39` for the pattern.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


SCORING_CONTRACT = {
    "matching": {
        "policy": "semantic_per_field (LLM-as-judge scores each field)",
        "rubric": {
            0: "Wrong — field is missing, has wrong key, or has a completely unrelated value (e.g., owner name in action field)",
            1: "Close — right concept but wrong detail (e.g., 'send Q3 plan' when expected 'send Q3 spec' — same intent, different noun)",
            2: "Correct — semantically equal to expected (paraphrase, slight rewording, or different but equivalent phrasing all accepted)",
        },
    },
    "none_policy": {
        "policy": "None means 'field absent', distinct from ''",
        "rubric": {
            0: "Hallucination — expected None but model returned a non-empty value (invented an action that wasn't there)",
            1: "Miss — expected a value but model returned None or empty (failed to extract)",
            2: "Correct — both None (no action to extract) OR both have values (use 'matching' rubric for value comparison)",
        },
    },
    "date_canonicalize": {
        "policy": "relative-as-string; freeze reference date if you ever canonicalize",
        "rubric": {
            0: "Format change — model converted date to a different format (e.g., 'Friday' → '2026-09-26' or 'Sep 25') when expected format was preserved",
            1: "Wrong day — model used a different day (e.g., expected 'next Tuesday', got 'next Wednesday')",
            2: "Preserved — model kept the date string as written (case-preserving, format-preserving)",
        },
    },
    "case_policy": {
        "policy": "owners are case-preserving as written ('Team' stays 'Team'); do not normalize",
        "rubric": {
            0: "Changed meaning — case change altered the identifier (e.g., 'Team' → 'TEAM' might lose specificity)",
            1: "Cosmetic — case normalization that didn't change meaning (e.g., 'John' → 'JOHN' — same person, different presentation)",
            2: "Preserved — case kept exactly as written in input",
        },
    },
}


def ready_tests() -> list[dict]:
    """Rows safe to run through the pipeline (TODO rows have None fields).

    run_eval.py and judge.py MUST consume this, not GOLDEN_DATASET —
    a TODO row sent to the model scores garbage and will send you down
    the wrong FAILURE TRIAGE branch.

    Returns:
        List of test dicts where provenance != "TODO". Each dict has
        non-None input/expected fields and is safe to feed to extract.py.
    """
    return [t for t in GOLDEN_DATASET if t.get("provenance") != "TODO"]


GOLDEN_DATASET = [
    {
        "id": "test-001",
        "dimension": "happy_path",
        "input": "John to send Q3 spec by Friday.",
        "expected": {
            "action": "send Q3 spec",
            "owner": "John",
            "due_date": "Friday",
        },
        "added_because": (
            "Exemplar: one action, one owner, one relative date. Baseline "
            "for what 'works' looks like. If this fails, the pipeline is "
            "broken."
        ),
        "provenance": "exemplar",
    },
    {
        "id": "test-004",
        "dimension": "negative_no_action",
        "input": "Q3 launch planning meeting.",
        "expected": {
            "action": None,
            "owner": None,
            "due_date": None,
        },
        "added_because": (
            "Exemplar: meeting title only, no actionable items. Tests null "
            "handling — system must NOT hallucinate an action from a title."
        ),
        "provenance": "exemplar",
    },

    # ---------------------------------------------------------------
    # USER rows — to be written by you as a learning exercise.
    # Dimensions are PRESCRIBED below; you write input/expected/source.
    # Recommended sourcing: your own real meeting notes (calendar, Slack,
    # transcripts) — that satisfies C2 (source from reality).
    # ---------------------------------------------------------------

    {
        "id": "test-002",
        "dimension": "implicit_owner",  # Step 4: prescribed
        "input": "Email team about the upcoming lunch on next Monday @ 12:30PM",
        "expected": {
            "action": "Email team about the upcoming lunch",
            "owner": None,
            "due_date": "next Monday @ 12:30PM"
        },
        "added_because": "Confirms system returns owner=None when no person is named. Does NOT rule out multi-action or hedged commitments.",
        "provenance": "user"
    },
    {
        "id": "test-003",
        "dimension": "past_tense_done",  # Step 6: prescribed
        "input": "John called Amy about the lunch yesterday.",
        "expected": {
            "action": None,
            "owner": None,
            "due_date": None
        },
        "added_because": "Confirms system returns None for past-tense actions. Does NOT rule out hedged commitments or multi-action inputs.",
        "provenance": "user"
    },
    {
        "id": "test-005",
        "dimension": "discussion_not_action",  # Step 6: prescribed
        "input": "Performance concerns were raised during the retro.",
        "expected": {
            "action": None,
            "owner": None,
            "due_date": None
        },
        "added_because": "Confirms system returns None for non-actionable discussion. Does NOT rule out hedged commitments or multi-action inputs.",
        "provenance": "user"
    },

    # ---------------------------------------------------------------
    # SCAFFOLDED rows (Step 8) — added for 9/9 dimension coverage.
    # Review and edit to match your real notes where applicable.
    # ---------------------------------------------------------------

    {
        "id": "test-006",
        "dimension": "missing_object",
        "input": "John to review.",
        "expected": {
            "action": "review",
            "owner": "John",
            "due_date": None,
        },
        "added_because": (
            "Confirms system extracts bare-verb actions without an object. "
            "Does NOT rule out multi-action inputs or hedged_commitment."
        ),
        "provenance": "user",
    },
    {
        "id": "test-007",
        "dimension": "iso_or_shorthand_date",
        "input": "Reply by COB Tuesday.",
        "expected": {
            "action": "reply",
            "owner": None,
            "due_date": "COB Tuesday",
        },
        "added_because": (
            "Confirms system preserves shorthand dates (COB/EOD/ASAP) "
            "as-written per date_canonicalize policy. "
            "Does NOT rule out hedged_commitment or multi_sentence."
        ),
        "provenance": "user",
    },
    {
        "id": "test-008",
        "dimension": "hedged_commitment",
        "input": "We might send the spec out Friday.",
        "expected": {
            "action": "send spec (tentative)",
            "owner": None,
            "due_date": "Friday",
        },
        "added_because": (
            "Confirms system treats tentative commitments ('might send') as "
            "action items per chosen SCORING_CONTRACT decision. "
            "Does NOT rule out missing_object or multi_sentence."
        ),
        "provenance": "user",
    },
    {
        "id": "test-009",
        "dimension": "multi_sentence",
        "input": "Caught up with John today. He mentioned the Q3 spec needs another pass — Sarah should look at the data model before sending it to the design team.",
        "expected": {
            "action": "review data model",
            "owner": "Sarah",
            "due_date": None,
        },
        "added_because": (
            "Confirms system can extract an action buried inside multi-sentence "
            "prose, ignoring surrounding context. "
            "Does NOT rule out hedged_commitment or iso_or_shorthand_date."
        ),
        "provenance": "user",
    },
]


if __name__ == "__main__":
    ready = ready_tests()
    total = len(GOLDEN_DATASET)
    print(f"ready: {len(ready)}/{total} tests ready ({total - len(ready)} TODO)")
    for t in GOLDEN_DATASET:
        print(f"  {t['id']} [{t['provenance']}] dim={t['dimension']}")
