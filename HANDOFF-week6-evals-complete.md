# Handoff — Week 6 (Evals) COMPLETE — next: Week 7 Observability Dashboard

## Where we are

Week 6 is **functionally complete and committed**. The eval pipeline is
fully operational: 15-row golden dataset → extract.py → judge.py →
run_eval.py harness → table + split-mean aggregate. README carries real
measured numbers. Plan targets met (15-20 pairs ✓, ≥6 dimensions ✓,
judge with rubric ✓).

**Date:** Sat Sep 26 2026
**Latest commit:** see `git log --oneline -5` — Week 6 evals commits end
with the dataset-growth + README-numbers commit.

## Where we left off

### Done this session (everything below is committed)

| Deliverable | File | Notes |
|---|---|---|
| run_eval.py harness (Steps 0-5) | `llm-practice/src/evals/run_eval.py` | table + aggregate + split means; timing instrumentation; council-reviewed (scout/reviewer/oracle round) with must-fixes applied |
| Orthogonal judge | `judge.py` | judge model = kimi-k3 (Moonshot), extractor = deepseek-v4.1-flash; self-preference bias MEASURED (see README) |
| POLICY MAP clarification | `judge.py` prompt | none_policy ONLY when expected field is None; expected-value + predicted-missing = matching rubric[0] = 0. Applied pre-baseline; negative rows 6/6 under both judges |
| temperature=0 in extract.py | `extract.py` | reproducibility; de-staled docstring (CONTRACT/DECISIONS/WHEN STUCK/EVAL-OF-EVAL) |
| Hardened bridge | `run_eval.py` Step 3 | first well-shaped item else all-None fallback; extract crashes → `extract-error:` rows (run survives) |
| Dataset growth 9 → 15 | `golden_dataset.py` | 6 new dimensions: relative_date_offset, time_only_deadline, fyi_not_action, passive_voice_action, owner_is_group, ambiguous_owner |
| README with real numbers | `llm-practice/src/evals/README.md` | the interview artifact — measured numbers, judge A/B, nondeterminism finding, "what we changed" |

### Key numbers (3 runs, n=15)

- mean blended 5.60–5.73 (±0.13 run-to-run)
- value rows 5.45–5.64 (n=11), negative rows 6.00 stable (n=4)
- ~3.3 min per full run (~13s/row, 2 LLM calls/row)

### Findings worth quoting in interviews

1. **Self-preference bias, measured** — same-family judge (deepseek) scored
   test-008 hedged-commitment 5; orthogonal judge (kimi-k3) scored 2 on
   identical extractor output. Honest conclusion: rubric ambiguity +
   same-company leniency, not "kimi is right."
2. **temperature=0 ≠ determinism** — test-001 drifted 6→3 between runs
   ("send"→"Send" capital flip, owner missed once). Rule adopted: report
   ranges over 2-3 runs, never single-run numbers.
3. **Judge variance exists too** — kimi scored test-008 2/5/6 across
   runs. Both sides of the pipeline are noisy; the aggregate is robust.

### Decisions made (don't re-derive)

| Decision | Choice | Why |
|---|---|---|
| test-015 gold (ambiguous_owner) | owner=None stands; "Raj or Dana" is an unresolved QUESTION, not a statement | User decision after seeing judge score passthrough as hallucination; passthrough would launder ambiguity into a person-field. Recorded in the row's `added_because`. |
| Synthesized inputs are OK | 6 growth rows marked `provenance: "synthesized"` | User has no real meeting feed — learning material. Comment block in golden_dataset.py documents this honestly (C2 caveat). |
| multi_action dimension | DEFERRED (option a) | Bridge judges only items[0]; adding a multi-action row needs the harness upgrade (expected→list, judge contract change) — a session of its own. RE-VISIT TRIGGER now live. |
| Hedged-commitment rubric | Still ambiguous (test-008 scores 2/5/6) | Open issue, disclosed in README. Fixing breaks score comparability — deliberate, documented, needs a session. |

## What's next

### Close-out checklist (if anything left uncommitted)

- `AGENTS.md` (repo-level instructions) — was untracked at session start; commit if still so
- `HANDOFF-week6-evals-judge-step5.md` — superseded by this file; keep for history, commit it
- Push to `main` if not yet done

### Week 7 (per the plan): Project 1 — Agent Observability Dashboard

~12-14h, the heavier week of the phase. Ideas carried over from Week 6
that feed directly in: trace/latency thinking (the perf_counter split),
error-row taxonomy (judge-error/extract-error), and "observability of
LLM calls" is literally what run_eval.py started. Read the Week 6
section of `ai-engineer-transition-plan.md` for the Week 7 spec before
scaffolding.

### Open technical items (optional, non-blocking)

1. Hedged-commitment rubric disambiguation (test-008) — the one live
   eval ambiguity.
2. `items[0]` bridge limitation — fires when multi_action row is added.
3. judge.py:69 docstring template still says deepseek (historical PATH
   record; the real call at :248 is kimi-k3). Cosmetic.
4. Deliberate-break test of judge.py never-raise contract — still never
   verified by execution.

## Key concepts drilled (this session)

- Dict subscript vs attribute access (`test["input"]` vs `test.input`) —
  AttributeError vs KeyError; per-hop type check after every `.`
- `list[dict]` vs `dict` return shapes — count is data; `[]` ≠
  all-None-dict; the bridge converts vocabularies
- Format spec mini-language — `:<9` / `:>7` = padEnd/padStart; `.2f`;
  widths are minimums; slice-before-format to keep columns aligned
- `time.perf_counter()` — monotonic clock for elapsed time
- Done-signals are contracts — must be satisfiable by actual code paths
  (caught twice: Step 0 and Step 2 of run_eval.py)
- Temperature=0 reduces but does not guarantee determinism
- Same-run judge variance vs cross-model judge bias — different tools
- mean vs pass rate; split means by row type; prefix-based error-row
  exclusion (never overall-based — error rows carry 0)

## Methodology that worked (match next session)

1. PATH-style scaffold docstring; user walks Steps hands-on, line by line
2. Concept deep-dives on demand (dict access, format specs, list-vs-dict)
3. Council review on new scaffolds — scout/reviewer/oracle round caught
   7 must-fixes before the user touched the code
4. User reviews agent-written code line by line and asks sharp questions
   ("where does input come from?", "why list not dict?") — this WORKED;
   they caught a real scaffold bug (Step 2 print) before I did
5. End-of-session handoff update (this file)

## User preferences (stable)

- Hands-on learner; runs scripts themselves; wants real output + real errors
- Hand-rolled code, no frameworks (refused LangChain; hand-rolled tables)
- Learning-artifact bar: clear intent, well-formatted, TODO markers with
  docstring hints saying exactly what to do
- Has JS/TS background — Python idioms land best when mapped to JS
  equivalents (padStart/padEnd, plain-object ≈ dict, undefined vs KeyError)
- Tires easily — tight closeouts, keep momentum
- Commit style: "Week 6 evals: <topic> (<changes>)" conventional commits

## Sensitive information

None. No keys/PII. API key stays in `.env` (OPENCODE_API_KEY via
find_dotenv()).

## Reference

- Plan: `ai-engineer-transition-plan.md` (source of truth; line ~229-232
  = Week 6 deliverables, line ~230 = stronger-model-grades-cheaper rule)
- Prior handoffs: `HANDOFF-week6-evals-judge-step5.md` (judge build),
  `HANDOFF-week6-evals-progress.md` (Sep 22 checkpoint)
- Scout context brief: `llm-practice/src/evals/CONTEXT-scout.md` (if
  present; else session artifacts dir)
- README with numbers: `llm-practice/src/evals/README.md`
