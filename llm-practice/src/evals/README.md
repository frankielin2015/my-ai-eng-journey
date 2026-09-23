# Week 6 — Evals

**Start here:** open `evals/golden_dataset.py` and read its module
docstring. Follow **Steps 0–8** in order. This README is the artifact you
write at the end, not the entry point.

## What we WILL measure (you decide)

By the end of Week 6, you will fill in this table. The numbers are blank
on purpose — your job is to produce them.

| metric | target | how we'll know |
|---|---|---|
| pairs in golden_dataset | 15–20 | `len(ready_tests())` |
| distinct dimensions covered | ≥6 of 9 | set comprehension over rows |
| judge policies with rubric | 4 of 4 | keys of JUDGE_RUBRIC |
| extractor F1 on golden | ___ | judge.py output |
| bounded-evidence failures caught | ___ | your row-level comments |

Do not write these numbers now. Write them after Steps 0–8.

## Why this matters

Week 5 gave us retrieval (pgvector + chunking + RAG). Week 6 asks: how do
we know if retrieval (or any LLM task) actually works? "It returned 3
hits" is not a quality signal — maybe all 3 are wrong. Evals turn "I
built a system" into "I built a system and can prove it works."

## Success test — answer BEFORE the table

What's the difference between a grader-based eval, a pairwise-comparison
eval, and a trajectory eval? When do you pick each?

Write three sentences here, then check yourself against the table below:

> Grader:
>
> Pairwise:
>
> Trajectory:

## Eval paradigms — when to pick each

| Paradigm | Question it answers | Pick when... |
|---|---|---|
| **Grader-based** | "Did the system get it right?" (single gold, absolute grading) | There is one defensible answer |
| **Pairwise comparison** | "Is A better than B?" (two prompts, no single gold, judge picks) | Quality is subjective |
| **Trajectory eval** | "Did the multi-step path succeed?" (agent + tools, judge scores the sequence) | What matters is the path, not just the final output |

This week's task (extraction from meeting notes) is **grader-based**: there
is one defensible gold answer per input. Pairwise and trajectory are
deferred to Weeks 7–8.

## What we changed (filled in after the eval runs)

_Pending — to be filled in after `judge.py` + `run_eval.py` exist and
you've run the eval at least once. **This is the section interviewers
will quote.** Plan line 232: "the single most-quoted-from document in
your interviews."_

## Files in this package

| File | Role | Status |
|---|---|---|
| `__init__.py` | Package marker, docstring | ✅ shipped |
| `extract.py` | The system under test (stub; wire up in Step 1.5) | 🚧 stub |
| `golden_dataset.py` | The (input, expected) pairs + scoring contract + `ready_tests()` guard | 🚧 2/5 shipped, 3 TODO |
| `judge.py` | LLM-as-judge: grades extract output vs `expected` per `SCORING_CONTRACT` | 🔜 next |
| `run_eval.py` | CLI: run extract() against golden, judge, report | 🔜 next |
