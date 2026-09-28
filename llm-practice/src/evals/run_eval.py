"""Week 6 — run_eval.py: the harness that ties extract.py + judge.py together.

This is the THIRD and final piece of the eval pipeline. It iterates
ready_tests() (NEVER raw GOLDEN_DATASET), runs the system under test
(extract.py), grades each output with the judge (judge.py), prints a
per-row table, then reports aggregate numbers — the numbers that go
into README.md's "What we changed" section (measured numbers + honest
interpretation).

DECISIONS (documented per judge.py's WHY THIS MATTERS convention):

- Models: extract = deepseek-v4.1-flash (DeepSeek), judge = kimi-k3
  (Moonshot) — an ORTHOGONAL judge, per the plan's "a stronger model
  grades the cheaper extractor" and to break *self-preference* bias
  (a same-company judge is lenient toward its own phrasing; extractor
  bugs and judge leniency would correlate and inflate the score).
  BASELINE for comparison: the same-model (deepseek both sides) run
  scored mean 5.44 blended — value rows 5.33 (n=6), negative rows 6.00
  (n=3). The orthogonal run's delta against THAT is the self-
  preference measurement. Keep the baseline in mind when quoting.
  Reverting = one string in judge.py's model= line.
- Bridge: extract_action_items() returns list[dict]; judge_one()
  takes ONE dict of shape {action, owner, due_date}. Hardened bridge
  and fallback in Step 3. Only the FIRST item of each row is judged.
  Verified: all 9 rows expect AT MOST 1 item (3 negative rows expect
  zero — those exercise the fallback branch). KNOWN LIMITATION: a
  multi-action row would judge a fraction of the output; RE-VISIT
  TRIGGER: the day the dataset gains a multi-action dimension.
- Extract failures: judge.py has a never-raise contract; extract.py
  does NOT (bare json.loads). The loop wraps the extract call — an
  extractor exception becomes a row with rationale "extract-error: ..."
  (overall 0), reported alongside the other error rows instead of
  killing the run and discarding completed rows.
- Aggregation policy: mean of overall (a 0-6 int — judge.py returns
  0, NEVER None, on error), 2 decimal places. Rows whose rationale
  starts with "judge-error:" or "extract-error:" are EXCLUDED from
  the means and reported separately. The mean is SPLIT two ways: over
  value-expected rows (6) and over all-None-expected rows (3). A
  single blended mean over this dataset shape is close to
  uninterpretable (the negative rows are nearly free points), so the
  README quotes the split, not the blend.

────────────────────────────────────────────────────────────────────────

Step 0 — Can you run this file?  (verb: run)

  do:   cd /Users/xiaofalin/WorkSpace/my-ai-eng-journey/llm-practice/src
        uv run python -m evals.run_eval
  done: prints "empty report: []" and exits 0 — no traceback, no LLM
        calls. This is a wiring check only: the imports resolve.
        (The stub rows arrive at Step 2; the real loop at Step 3.)

────────────────────────────────────────────────────────────────────────

Step 1 — Read the contract  (verb: read)

  do:   Read `run_eval()`'s docstring below, then look at the pieces
        it consumes:
          - golden_dataset.ready_tests()  → list[dict], filter of
            GOLDEN_DATASET (NEVER feed raw TODO rows to the model)
          - extract.extract_action_items(text) → list[dict]
          - judge.judge_one(input, predicted, expected) → dict
            {"scores": {...}, "rationale": str, "overall": int}
        run_eval() must NOT re-implement any of these — only sequence
        them. If logic wants to live in run_eval(), it belongs in
        extract.py or judge.py instead.
  done: you can describe the data flowing through the loop, in order:
        test dict → input string → extracted items → predicted dict →
        judged result dict → accumulated row.

────────────────────────────────────────────────────────────────────────

Step 2 — Stub the report  (verb: write)

  do:   In `run_eval()`, find the `# TODO Step 2:` marker. Replace
        `return []` with HARDCODED results for 2 rows in the shape
        the loop will produce (one perfect, one judge-error — note
        judge.py returns overall=0 on error, NEVER None):
          rows = [
            {"id": "test-001", "dimension": "happy_path",
             "negative": False, "overall": 6,
             "rationale": "stub: perfect"},
            {"id": "test-004", "dimension": "negative_no_action",
             "negative": True, "overall": 0,
             "rationale": "judge-error: stub forced"},
          ]
          return rows
        Exclusion from the means is keyed on the rationale PREFIX
        ("judge-error:" / "extract-error:"), not on overall.
  done: `uv run python -m evals.run_eval` prints the raw list with
        the 2 stub rows. (The formatted table + aggregate lines come
        with Steps 4-5 — until then, __main__ prints the raw list.)

────────────────────────────────────────────────────────────────────────

Step 3 — Real loop: extract → bridge → judge  (verb: write)

  do:   Replace the stub with the real loop over ready_tests():
          for test in ready_tests():
              try:
                  items = extract_action_items(test["input"])
                  # BRIDGE — extract gives a LIST, judge takes ONE
                  # dict of shape {action, owner, due_date}. Guard
                  # the shape; the all-None fallback IS judge.py's
                  # documented predicted shape (values may be None).
                  predicted = (items[0] if isinstance(items, list)
                               and items
                               and isinstance(items[0], dict)
                               else {"action": None, "owner": None,
                                     "due_date": None})
                  result = judge_one(test["input"], predicted,
                                     test["expected"])
              except Exception as err:   # extract.py CAN raise!
                  result = {"overall": 0,
                            "rationale": f"extract-error: {err}"}
              rows.append({
                  "id": test["id"],
                  "dimension": test["dimension"],
                  "negative": test["expected"]["action"] is None,
                  "overall": result["overall"],
                  "rationale": result["rationale"],
              })
  done: 9 rows come back with real LLM calls (extract=deepseek-v4.1-flash,
        judge=kimi-k3 — orthogonal judge, see DECISIONS).
        Expect a handful of seconds per row — 9 rows is slow enough
        to be visible, fast enough to not need parallelism.

────────────────────────────────────────────────────────────────────────

Step 4 — Per-row table  (verb: write)

  do:   Print the accumulated rows as a table. Print ID, dimension,
        overall, then a SHORTENED rationale (first ~60 chars — LLM
        rationales get long; use slicing, not truncation words).
        Keep the function RETURNING `rows` (dicts, not strings):
        printing is a side effect; the data belongs to the caller.
  done: a readable 9-line table you can screenshot into the README.

────────────────────────────────────────────────────────────────────────

Step 5 — Aggregate + error exclusions + split means  (verb: write)

  do:   BELOW the table, compute:
          - total rows
          - excluded = rows whose rationale starts with
            "judge-error:" or "extract-error:"
          - eligible mean overall across the rest, round(.., 2)
        Then the SPLIT (why: the 3 all-None-expected rows are nearly
        free points — a blended mean hides more than it shows):
          - mean over rows where negative is False (6 value rows)
          - mean over rows where negative is True (3 negative rows)
        Print e.g.:
          mean overall: 5.11 over 9/9 rows (0 excluded)
          mean (value rows):    5.50  n=6
          mean (negative rows): 4.33  n=3
        Guard EVERY division with an `if` (if ALL rows are excluded,
        print the count and do NOT compute any mean).
  done: each line matches the table (spot-check one row of each kind
        by hand). These three numbers go into README.md.

────────────────────────────────────────────────────────────────────────

## WHERE to write the code

All edits happen INSIDE `run_eval()` below. Look for the TODO markers:
    # TODO Step 2: ...
    # TODO Step 3: ...
    # TODO Step 4: ...
    # TODO Step 5: ...
Step 2 replaces `return []`. Steps 3-5 replace Step 2's lines.

────────────────────────────────────────────────────────────────────────

## WHEN YOU GET STUCK

- `ModuleNotFoundError: No module named 'client'` → run from inside
  src/ (the path shim below handles the sibling import).
- Only 2 rows printed, both hardcoded → Step 2's stub is still in
  place; do Step 3.
- `KeyError: 'overall'` → you're reading something other than
  judge_one's return (e.g., the raw LLM JSON). judge_one ALWAYS
  includes 'overall' — trust the contract.
- Every row prints judge-error → the JUDGE call failed (API key or
  model name). NOTE: extract.py raising would CRASH the run with a
  traceback, not produce judge-error rows — they're different failure
  surfaces (extract crashes become "extract-error:" rows via Step 3's
  try/except).
- Mean comes out as 0 for everything → you're averaging the wrong
  field, or including error rows. Check the rationale-prefix filter.
  judge.py already guarantees overall is a 0-6 int — trust it.
- A REAL score of 0 somewhere (test-004 / test-003 / test-005 are
  None-expected rows) → NOT an exception. Per none_policy rubric[0],
  that means the extractor HALLUCINATED an action where there was
  none. That is signal, not a bug in the harness. FAILURE TRIAGE:
  test wrong → too strict → system broken, in that order.

## WHY THIS MATTERS

Grader-based eval only becomes USEFUL when it's cheap to re-run:
that's what makes "iterate the eval, not just the system" possible
(Week 6 concept C4). This file is the cheap knob — 1 command, one
number to track over time. Everything downstream (README numbers,
dataset-growth decisions, model swaps) reads this output.

The aggregate is a MEAN, not a pass rate: 0/1/2 scores carry
gradations (close-but-wrong ≠ hallucinated), and a mean preserves
them. With n=9, one row dropping costs ~0.7 — small enough that you
see it, big enough that one row can't be the whole story.

EVAL OF THE EVAL: spot-check 5 rows against the rationale column
before quoting the mean anywhere. If you disagree with the judge,
the rubric is wrong — fix SCORING_CONTRACT, rerun, and note the
change breaks comparability with past scores.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

# Repo convention: every module under src/ needs this shim to find sibling
# packages. See week5/query.py:30 and evals/extract.py for the pattern.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from evals.extract import extract_action_items
from evals.golden_dataset import ready_tests
from evals.judge import judge_one


def run_eval() -> list[dict]:
    """Run extract → judge across ready_tests(); accumulate rows.

    Returns:
        A list of per-row result dicts, one per ready test:
            {"id": str, "dimension": str, "negative": bool,
             "overall": int, "rationale": str}
        overall is ALWAYS an int (judge.py returns 0, never None,
        on error). Error rows are excluded from aggregate means by
        their "judge-error:" / "extract-error:" rationale prefix.
    """
    rows = []                       # accumulator: one result dict per row
    # TIMING (debug aid): perf_counter is a monotonic high-res clock —
    # the right tool for elapsed time (time.time() can jump if the OS
    # syncs its clock mid-run). Each row = extract + judge, 2 LLM calls.
    run_start = time.perf_counter()
    for test in ready_tests():
        row_start = time.perf_counter()
        try:
            items = extract_action_items(test["input"])
        except Exception as err:    # extract.py CAN raise (bare json.loads)!
            # Never let row 3 kill rows 1-2: convert the crash into an
            # "extract-error:" row so Step 5 can exclude it from means.
            rows.append({
                "id": test["id"],
                "dimension": test["dimension"],
                "negative": test["expected"]["action"] is None,
                "overall": 0,
                "rationale": f"extract-error: {type(err).__name__}: {err}",
            })
            continue                # skip extract/judge for this row only

        # BRIDGE — extract speaks list[dict] (real-world: variable count),
        # judge speaks ONE dict (golden dataset: single expected item).
        predicted = (items[0] if isinstance(items, list) and items and isinstance(items[0], dict)
                     else {"action": None, "owner": None, "due_date": None})
        result = judge_one(test["input"], predicted, test["expected"])

        rows.append({
            "id": test["id"],
            "dimension": test["dimension"],
            "negative": test["expected"]["action"] is None,  # drives Step 5's split means
            "overall": result["overall"],   # judge.py guarantees int 0-6 — trust it
            "rationale": result["rationale"],
        })
        print(f"  {test['id']} done in {time.perf_counter() - row_start:.1f}s")

    total = time.perf_counter() - run_start
    print(f"  TOTAL: {total:.1f}s for {len(rows)} rows "
          f"({total / max(len(rows), 1):.1f}s/row avg)")

    # ── Step 4: per-row table ────────────────────────────────────
    # Hand-rolled f-string columns (no tabulate on purpose). Header,
    # then one line per row: id, negative flag, overall, short rationale.
    # Rationale sliced [:60] — LLM rationales get long; the full text
    # stays in `rows` (the machine view __main__ prints).
    print("\nPER-ROW RESULTS")
    print(f"{'id':<9} {'dim':<22} {'neg':>3} {'overall':>7}  rationale")
    print("-" * 78)
    for r in rows:
        print(f"{r['id']:<9} {r['dimension'][:22]:<22} "
              f"{str(r['negative'])[0]:>3} {r['overall']:>7}  "
              f"{r['rationale'][:60]}")

    # ── Step 5: aggregate + error exclusions + split means ──────
    # Exclusion is keyed on the rationale PREFIX ("judge-error:" /
    # "extract-error:") — NEVER on overall (error rows carry 0, and
    # folding them into the mean would drag the headline number down
    # silently). Split means because the 3 negative rows are nearly
    # free points: a blended mean hides more than it shows.
    total_n = len(rows)
    excluded = [r for r in rows
                if r["rationale"].startswith(("judge-error:", "extract-error:"))]
    eligible = [r for r in rows if r not in excluded]

    print("\nAGGREGATE")
    print(f"rows: {total_n}, excluded (error rows): {len(excluded)}")
    if eligible:
        mean_all = sum(r["overall"] for r in eligible) / len(eligible)
        print(f"mean overall: {mean_all:.2f} over "
              f"{len(eligible)}/{total_n} rows ({len(excluded)} excluded)")
    else:
        print("mean overall: N/A — ALL rows excluded (error rows only)")

    # Split means, guarded independently: each side must have rows
    # AND none of them excluded before a mean is meaningful.
    value_rows = [r for r in eligible if not r["negative"]]
    neg_rows = [r for r in eligible if r["negative"]]
    if value_rows:
        print(f"mean (value rows):    "
              f"{sum(r['overall'] for r in value_rows) / len(value_rows):.2f}  "
              f"n={len(value_rows)}")
    else:
        print("mean (value rows):    N/A — no eligible value rows")
    if neg_rows:
        print(f"mean (negative rows): "
              f"{sum(r['overall'] for r in neg_rows) / len(neg_rows):.2f}  "
              f"n={len(neg_rows)}")
    else:
        print("mean (negative rows): N/A — no eligible negative rows")

    return rows


if __name__ == "__main__":
    rows = run_eval()
    if not rows:
        # Step 0 state: wiring check only — make the silence truthful.
        print("empty report: []")
    else:
        # Step 2 state: show the raw stub rows. From Step 4-5 on,
        # run_eval() prints the formatted table itself, so this raw
        # dump becomes the debug view (table = human report,
        # list-of-dicts = machine data — same rows, two views).
        print(rows)
