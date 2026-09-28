# Week 6 — Evals

**Start here:** open `evals/golden_dataset.py` and read its module
docstring. Follow **Steps 0–8** in order. This README is the artifact you
write at the end, not the entry point.

## What we measured (real numbers, Sept 26 2026 runs)

Task: extract `{action, owner, due_date}` from short meeting notes
(grader-based eval, one gold per input). System under test:
`extract.py` (deepseek-v4.1-flash, temperature=0). Judge: `judge.py`
(LLM-as-judge vs `SCORING_CONTRACT`, 0-2 per field, overall 0-6).

| metric | value | how measured |
|---|---|---|
| pairs in golden_dataset | **15** (plan target 15-20 ✓) | `len(ready_tests())` |
| distinct dimensions covered | **15/15** | one per row |
| judge policies with rubric | 4 of 4 | keys of `SCORING_CONTRACT` |
| mean overall (blend, 3 runs) | **5.60–5.73** | `run_eval.py` aggregate |
| mean overall — value rows (n=11) | **5.45–5.64** | split mean |
| mean overall — negative rows (n=4) | **6.00 (stable across all runs)** | split mean |
| full run latency | ~3.3 min for 15 rows (~13s/row, 2 LLM calls/row) | `perf_counter` timing |
| run-to-run variance (blended) | ±0.13 over 3 runs | repeat runs — the reason we report ranges |

### The judge A/B experiment (same-model vs orthogonal judge)

The extractor's own model family (deepseek) graded its output first,
then a different company's model (kimi-k3) graded the SAME extractor
outputs. Same scores everywhere except the ambiguous rows:

| row | deepseek judge | kimi-k3 judge | what it exposed |
|---|---|---|---|
| 7 unambiguous rows | 6/6 | 6/6 | consensus — solid signal |
| test-002 (implicit_owner) | 3 | 4 | judge disagreement on "action absorbed the date" |
| test-008 (hedged_commitment) | **5** | **2** | same-company judge lenient toward its own phrasing → **self-preference bias, measured** |

Reading: the same-model judge resolved an under-specified rubric case
("send spec" vs "send spec (tentative)") in its own output's favor.
The orthogonal judge applied the letter of the rubric (missing expected
value = 0). The honest conclusion is NOT "kimi is right" — it is that
**the hedged-commitment rubric is ambiguous, and which model you use
decides the answer today.** Fix pending: disambiguate SCORING_CONTRACT
(breaks comparability with the numbers above — documented, deliberate).

### Finding: temperature=0 is not a determinism guarantee

Same input, same model, seconds apart:

```
run 1: [{'action': 'send Q3 spec', 'owner': 'John', ...}]
run 2: [{'action': 'Send Q3 spec', 'owner': 'John', ...}]   # ← capital flip
```

`temperature=0` reduces sampling randomness; gateway/routing variance
remains. Consequences we operate by:

1. A single eval run is **one sample, not the truth** (test-001 scored
   6, then 3, across runs — the extractor drifted, not the system).
2. Report **means over 2-3 runs** (or the range) when claiming a
   prompt change helped; otherwise noise can flip a row.
3. Cheap re-runs (~90s) are what make measuring variance practical —
   that's the point of a harness.

## What we changed (based on eval results)

1. **POLICY MAP clarification in judge.py** — the original composition
   rule (`none_policy first, else matching`) never said WHEN
   none_policy applies. A completely-broken extractor could therefore
   score 33-67% depending on judge whim (both readings were
   textually supported). Fixed pre-baseline (free — no past scores to
   break): *none_policy applies ONLY when the expected field is None;
   expected-value + predicted-missing = matching rubric[0] = 0.*
   Verified: all 3 negative rows now score 6/6 under BOTH judges —
   zero ambiguity left there.
2. **temperature=0 in extract.py** — after the drift finding above.
   Without it, the README's "what we changed" story can't separate a
   prompt improvement from sampling noise.
3. **Orthogonal judge (kimi-k3)** — one-string change in judge.py.
   Converts the documented self-preference liability into the
   measured A/B table above.
4. **Hardened bridge in run_eval.py** — extractor returns `list[dict]`
   (real-world shape: variable count), judge takes ONE dict. Bridge:
   first item if well-shaped, else all-None fallback (the documented
   `predicted` shape). Known limitation: only `items[0]` is judged —
   fires the re-visit trigger the day a multi-action row is added.
5. **Extract-error isolation** — extract.py deliberately has NO
   never-raise wrapper (judge.py owns that contract; separate failure
   surfaces stay visible). run_eval.py wraps the extract call instead:
   a crash becomes an `extract-error:` row, excluded from means, and
   rows 1-2 survive.

### What the eval caught (eval doing its job)

- **test-002 scored 3/6 consistently across ALL runs and BOTH judges**: the extractor absorbs "next Monday @ 12:30PM" into the action string and misses `due_date` as its own field. Real extraction bug, caught by the rubric, fully reproducible.
- **test-015 (ambiguous_owner)**: extractor passed "Raj or Dana" through verbatim; judge scored 0 (none_policy rubric[0]: expected None, got a value). User decision on the gold: **owner=None stands** — "Raj or Dana" is an unresolved question, not an owner statement; passthrough would launder ambiguity into a person-field. (Decision recorded in the row's `added_because`.)
- **test-008 (hedged)**: judged differently across runs AND models (2/5/6) — rubric under-specification for hedged commitments remains the one open eval issue. (FAILURE TRIAGE: test wrong? → too strict? → system broken? Here: rubric ambiguous.)
- **test-007**: dropped 'Tuesday' from 'COB Tuesday' in one run (5/6) — extractor drift, the nondeterminism finding in action.

## Why this matters

Week 5 gave us retrieval (pgvector + chunking + RAG). Week 6 asks: how do
we know if retrieval (or any LLM task) actually works? "It returned 3
hits" is not a quality signal — maybe all 3 are wrong. Evals turn "I
built a system" into "I built a system and can prove it works."

## Success test — the three paradigms

> **Grader:** one defensible gold answer per input; score the output
> absolutely against it. Pick when quality has a right answer.
>
> **Pairwise:** two candidate outputs, no single gold; a judge picks
> the better. Pick when quality is subjective/comparative.
>
> **Trajectory:** judge the multi-step path (agent + tool calls), not
> just the final output. Pick when the process is the product.

This week's task is **grader-based**. Pairwise and trajectory are
deferred to Weeks 7-8.

| Paradigm | Question it answers | Pick when... |
|---|---|---|
| **Grader-based** | "Did the system get it right?" (single gold, absolute grading) | There is one defensible answer |
| **Pairwise comparison** | "Is A better than B?" (two prompts, no single gold, judge picks) | Quality is subjective |
| **Trajectory eval** | "Did the multi-step path succeed?" (agent + tools, judge scores the sequence) | What matters is the path, not just the final output |

## Files in this package

| File | Role | Status |
|---|---|---|
| `__init__.py` | Package marker, docstring | ✅ shipped |
| `golden_dataset.py` | 15 (input, expected) pairs + `SCORING_CONTRACT` + `ready_tests()` guard | ✅ shipped (plan target met) |
| `extract.py` | The system under test (deepseek-v4.1-flash, temp=0) | ✅ shipped |
| `judge.py` | LLM-as-judge (kimi-k3, orthogonal) vs `SCORING_CONTRACT`, never-raise | ✅ shipped |
| `run_eval.py` | Harness: extract → judge → table + aggregate + split means | ✅ shipped |

## Run it

```bash
cd llm-practice/src && uv run python -m evals.run_eval
```
