# Handoff — Week 6 (Evals): extract.py + judge.py complete, run_eval.py next

## Where we are

User is mid-Week 6 of `ai-engineer-transition-plan.md`. Week 5 (pgvector + RAG fundamentals) and the prior evals-progress checkpoint (`HANDOFF-week6-evals-progress.md` from Sep 22) are complete and on `main`. **As of Sep 26:** all 5 concepts from Anthropic's "Develop test cases" doc have been walked through, `extract.py` is a working LLM call, `judge.py` reached **Step 5 of its PATH (defensive validation)** and is fully runnable. **What's left for Week 6:** `run_eval.py` (the harness), the first scored run, README update with real numbers, and optionally growing the dataset from 9 → 15-20 rows.

**Date:** Sat Sep 26 2026
**Latest commit on main:** `cddd214 chore: remove project-level skills lockfile (skills now installed globally via ~/.agents)` (housekeeping, between sessions)

**Week 6 commits on main (in order):**
```
96b7a24  Week 6 evals: judge.py Steps 3-5 (LLM call + POLICY MAP rubric + defensive validation)
b06c272  Week 6 evals: judge.py scaffold + council fixes (POLICY MAP, judge-error marker, self-preference)
2a20724  Week 6 evals scaffold: 9-row golden dataset, SCORING_CONTRACT rubric, extract.py stub
728c867  Week 6 handoff: progress checkpoint before eval scaffolding
```

## Where we left off

### Done

| Deliverable | File | Status |
|---|---|---|
| Golden dataset (9 rows / 9 dimensions / unified SCORING_CONTRACT) | `llm-practice/src/evals/golden_dataset.py` | ✓ shipped |
| Extractor (LLM call, hand-rolled, returns `list[dict]`) | `llm-practice/src/evals/extract.py` | ✓ shipped — but docstring still says "stub" (stale; functional) |
| LLM-as-judge (Steps 0-5 PATH complete) | `llm-practice/src/evals/judge.py` | ✓ shipped |
| Env-loading portability fix | `llm-practice/src/client.py` (uses `find_dotenv()`) | ✓ shipped |
| Eval package marker | `llm-practice/src/evals/__init__.py` | ✓ shipped |
| Eval README (placeholder, needs real numbers) | `llm-practice/src/evals/README.md` | 🔲 placeholder only |

### In progress / pending

| Item | Notes |
|---|---|
| **`run_eval.py`** — the harness | Not started. Iterates `ready_tests()`, calls extract → judge, prints table + aggregate. **Biggest remaining piece.** |
| First scored run on all 9 rows | After run_eval.py lands. |
| README "What we measured" section | Update with real numbers from the first scored run. |
| Dataset growth (plan target: 15-20 pairs) | Currently 9 rows / 9 dimensions; need 6-11 more for plan target. Optional but plan-aligned. |
| Polish: `extract.py` docstring still says "stub" | Cosmetic; doesn't affect function. |
| Polish: `judge.py` prompt has `PREDICTED: ...` + `Return JSON only...` running together (no `\n`) | Cosmetic; LLM handled it fine. |

### Decisions made (with rationale — don't re-derive)

| Decision | Choice | Why |
|---|---|---|
| Eval target | **Option A**: extract `{action, owner, due_date}` from meeting notes | Plan's example; concrete deliverable; doesn't depend on Week 5 RAG being up. |
| Eval paradigm | **Grader-based** (single gold per input) | Plan called for this; pairwise/trajectory deferred to later weeks. |
| Model | **`deepseek-v4.1-flash`** for both extract.py and judge.py | User picked it during Step 3 walkthrough; cheaper than kimi-k2. Same-model has self-preference risk — documented in judge.py's WHY THIS MATTERS. |
| Number of rows | **9 (2 exemplars + 3 user + 4 scaffolded)** | Reaches 9/9 dimensions, the floor for a credible eval. Plan target 15-20 deferred. |
| `SCORING_CONTRACT` shape | Unified dict per policy: `{policy: <str>, rubric: {0: <str>, 1: <str>, 2: <str>}}` | User pushed back on having two parallel dicts (`SCORING_CONTRACT` + `JUDGE_RUBRIC`); one dict per policy with both halves is cleaner. |
| Hedged commitment policy | "We might send the spec out Friday" → treated as an action item with `(tentative)` marker | Documented in `added_because` of test-008. User can re-decide. |
| Sanitization on judge input | **Delimiters `<<<\n...\n>>>` + `input_text[:2000]` cap** | User added during Step 5 walkthrough (took Option 2 instead of Option 1). Cheap insurance. |
| `extract.py` schema | Returns `list[dict]`, each `{action, owner, due_date}` | Matches judge's `predicted: dict` shape with the bridge: `predicted = extract_action_items(input)[0]` (run_eval.py will need this). |

### Council reviews done

Two rounds of council (kimi + grok + deepseek) reviewed the **judge.py scaffold**. 7 must-fixes applied:

1. Step 4 rubric-inverted claim fixed (`0/6` → correct `6/6` + `4/6` expectations)
2. Step 4 f-string `\\n` → `\n` (real newlines in prompt)
3. Step 4 added **POLICY MAP composition rule** (`none_policy` first, else min of applicable policies) — was the highest-leverage correctness fix
4. Step 5 wraps **entire body** in `try/except Exception` (not just `json.loads`); recomputes `overall` in Python; `"judge-error:"` prefix for downstream exclusion
5. Step 3 added `temperature=0` + "print `content` once" debug note
6. `judge_one()` docstring clarified `predicted` as "one predicted item dict — a single element of `extract_action_items()`'s list output"
7. WHY THIS MATTERS section names **self-preference bias** + adds "spot-check 5 rows yourself" (eval of the eval)

Council-flagged **future work** (NOT applied this session):
- `response_format={"type": "json_schema"}` migration (replaces fence-strip + coerce with provider-enforced JSON)
- Same-model vs orthogonal-model judge experiment
- Few-shot exemplars / chain-of-thought in judge prompt (explicitly out-of-scope for this scaffold)
- `extract.py` returns `list[dict]` vs `judge_one` takes `dict` shape mismatch — to be resolved in `run_eval.py`

## What's next

### Immediate next step: build `run_eval.py`

Same PATH-style scaffold as `golden_dataset.py` and `judge.py`. Suggested Steps:

- **Step 0** — `uv run python -m evals.run_eval` prints stub table
- **Step 1** — Read the contract: iterate `ready_tests()`, call extract, call judge, accumulate
- **Step 2** — Stub the loop body (hardcoded table for 2-3 rows)
- **Step 3** — Real loop: call `extract_action_items(test["input"])` → `predicted = items[0] if items else {}` → call `judge_one(test["input"], predicted, test["expected"])`
- **Step 4** — Per-row table output (id, dimension, per-field scores, overall, rationale)
- **Step 5** — Aggregate: total rows, mean overall (excluding `judge-error:` rows separately)

### Then: first scored run

```bash
cd llm-practice/src && uv run python -m evals.run_eval
```

Expected output: per-row table, then aggregate. Likely 6-9 rows scoring well, 1-3 scoring low (test-004, test-008 hedging, test-009 multi-sentence). Real numbers go into the README.

### Then: README update

`llm-practice/src/evals/README.md` currently has placeholder text. After first scored run, fill in:
- "What we measured" with actual numbers
- "What we learned" with at least one prompt or dataset change based on results
- This is the **interview-quote-worthy** artifact per the plan

### Optional: dataset growth

Plan target 15-20 rows. Currently 9. To grow, add rows in `GOLDEN_DATASET` for dimensions user finds interesting (multi-action, ambiguous owner, paraphrased dates, etc.). One dimension per row.

### After Week 6: Week 7

Per the plan, Week 7 is **Project 1: Agent Observability Dashboard** (~12-14 hours, the heavier week of the phase).

## Key concepts drilled (Week 6 cumulative)

### Eval methodology (5 concepts from "Develop test cases")

| # | Concept | Status |
|---|---|---|
| 1 | Bounded evidence, not proof (corrected framing — user pushed back on "claim") | ✓ |
| 2 | Source from reality | ✓ (user-written inputs from real meeting notes) |
| 3 | Diversity beats volume (5 dimensions × N rows each) | ✓ (9/9 dimensions covered) |
| 4 | Iterate the eval, not just the system (FAILURE TRIAGE: TEST WRONG → TEST TOO STRICT → SYSTEM BROKEN) | ✓ |
| 5 | Build incrementally (2 → 5 → 9 rows; never jumped straight to 20) | ✓ |

### LLM-as-judge concepts (new this session)

- **Prompted JSON is a request, not a constraint** — see it fail with the loose prompt (Step 3), then see it work with rubric + POLICY MAP (Step 4). Visible difference: 0/1 floats + hallucinated `field_accuracy`/`exact_match` (Step 3) vs. clean 0/1/2 integers + only the 3 expected keys (Step 4).
- **Rubric composition** — 4 policies in SCORING_CONTRACT → 3 field scores out. Composition rule: `none_policy` first, else `min(applicable policies)`. The most pessimistic wins.
- **Self-preference bias** — same model grading its own output is lenient toward its own phrasing. Errors correlate and the eval looks better than it is. Run judge with a different model to expose.
- **Never-raise contract** — judge wraps entire body in `try/except Exception`; returns stub with `"judge-error:"` prefix; `run_eval.py` excludes these rows from aggregate scores.
- **Recompute, don't trust** — LLM's `overall` is a hallucinated extra field; sum the per-field scores in Python instead.
- **Eval of the eval** — spot-check 5 rows manually; if you disagree with the judge, the rubric is wrong, not the model.

### Python idioms clarified this session

- `json.loads()` returns Python-native types (`dict`, `list`, `int`, etc.), not "JSON objects" — JSON is the wire format, dict is the in-memory form
- `dict.get(key, default)` — safe accessor; `["key"]` raises on missing
- `for field in ("a", "b", "c")` — tuple literal whitelist vs `for field in d.keys()` — discovers keys. Different intents: whitelist enforces schema, discover exposes data.
- `int(x)` raises `ValueError`/`TypeError` on garbage; defensive code uses try/except to coerce
- `max(0, min(2, v))` — clamp pattern
- `sum(scores.values())` — recompute aggregate from source

## Methodology / ceremony that worked

The user walked through **every file** using a consistent pattern. **Match this for `run_eval.py`** — the user expects it.

1. **Scaffold with a PATH-style docstring** at the top of the file. Steps 0-N with `verb + do + done` for each. Reference `extract.py:112-119` or `judge.py:55-81` for line-citable templates.
2. **User does the Steps hands-on.** They edit the function body per the docstring. They run scripts themselves. Don't run for them.
3. **Concept deep dives on demand.** When the user asks "why is this this way?", explain the underlying concept (e.g., prompted JSON is a request not a constraint), not just the syntax.
4. **Council review on new scaffolds.** When scaffolding a new file (e.g., `run_eval.py`), dispatch a 3-councillor review (kimi + grok + deepseek) before declaring it done. Apply the must-fixes.
5. **`@quick` for git work.** Commit + push via `@quick` subagent. Style: "Week 6 evals: <topic> (<changes>)".
6. **End-of-session handoff.** Update the HANDOFF-*.md chain. Don't rely on chat history.

## User preferences

- Hands-on learner; runs scripts themselves; wants to see actual output + actual errors
- Prefers hand-rolled code over library suggestions (e.g., refused LangChain earlier; `extract.py` uses raw `chat.completions` + manual `json.loads`)
- Tires easily — keep momentum, tight closeouts
- Simple input pattern (1-2 sentence meeting notes, ~5-10 words)
- Reads code carefully and asks sharp questions ("why don't we use a full JSON schema?" — caught a real prompt ambiguity)
- Catches terminology issues (e.g., "parsed is a dict, not a JSON object?" — was right)
- For commit work: delegate to `@quick`
- For council reviews: dispatch 3 councillors in parallel, then synthesize via `council` agent

## Known issues / quirks

1. **`extract.py` docstring still says "stub"** — code is functional; docstring is stale. ~30-second fix when in `run_eval.py`.
2. **`judge.py` prompt has PREDICTED JSON and "Return JSON only" on the same line** (no `\n` between them) — LLM handled it; cosmetic. ~30-second fix.
3. **Shape mismatch to resolve in `run_eval.py`**: `extract.py` returns `list[dict]`, `judge_one` takes `dict`. Bridge: `predicted = items[0] if items else {}`. Decide explicitly.
4. **Deliberate-break test for judge.py** (force prose from LLM) — user didn't run it; defensive layer code is correct by inspection but unverified by execution. Optional verification.

## Suggested skills for the next agent

- `handoff` — to re-compact this handoff if a third laptop is added
- `verification-planning` — before implementing `run_eval.py` (the eval pipeline is non-trivial; worth a verification plan)
- `simplify` — after the eval pipeline works, for cleanup pass on the code
- `teach` — if the next agent should match the "concept deep dives on demand" tutoring style
- `code-review` — to review `run_eval.py` once written (lighter than full council; 2-axis Standards + Spec)
- `worktrees` — only if the user wants an isolated lane (probably not needed; single-developer repo)
- `oh-my-opencode-slim` — only if user requests tuning of agent behavior

## Sensitive information

None included. No API keys, no passwords, no PII. The repo uses local Ollama for embeddings and OpenCode Go (already configured) for chat — no secrets to redact.

## Reference

- Plan file: `ai-engineer-transition-plan.md` (in repo root)
- Week 6 section in the plan: search for "Week 6" or "evals" or "golden dataset"
- Prior handoff: `HANDOFF-week6-evals-progress.md` (Sep 22, before judge.py)
- Anthropic docs to read next (still relevant): https://platform.claude.com/docs/en/test-and-evaluate/define-success
- Anthropic docs already covered: "Develop test cases" (all 5 concepts walked through)
- GitHub: https://github.com/frankielin2015/my-ai-eng-journey

## Concrete actions for the next agent

1. **Acknowledge the user's hands-on preference** at the start. Confirm they're driving, you're scaffolding + reviewing.
2. **Scaffold `run_eval.py`** with the PATH-style docstring + Steps 0-5. Mirror the ceremony of `judge.py` exactly.
3. **User walks through Steps 2-5 hands-on.** They edit, run `uv run python -m evals.run_eval`, see output.
4. **Run a council review** on the `run_eval.py` scaffold before declaring it done.
5. **Apply council must-fixes**, commit via `@quick`.
6. **Run the eval end-to-end** on the 9 rows. Capture the per-row output for the README.
7. **Update `llm-practice/src/evals/README.md`** with the measured numbers and what was learned.
8. **Commit + push** the README update.
9. **Optional**: grow the dataset (6-11 more rows) to reach plan target. Optional: do the cosmetic fixes (`extract.py` docstring, `judge.py` newline quirk).
10. **Plan Week 7** when Week 6 is wrapped: **Project 1 — Agent Observability Dashboard** (~12-14 hr heavier week per the plan).
