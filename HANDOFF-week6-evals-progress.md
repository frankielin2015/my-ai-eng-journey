# Handoff — Week 6 (Evals) progress

## Where we are

Started Week 6 of `ai-engineer-transition-plan.md`. Week 5 (pgvector + RAG fundamentals) is complete and on `main`. Currently mid-concept-walkthrough on the Anthropic **"Develop test cases"** doc, before any code is written.

**Date:** Tue Sep 22 2026
**Latest commit on main:** `da28993` — Week 5 exercises 7-10

## What's been done in Week 6 so far

### Reading
- ✅ **Anthropic: Develop test cases** — read, concepts walked through
- 🔲 **Anthropic: Define success** — NOT read yet; recommended before next session
- 🔲 Anthropic cookbook notebook (run it, ~60 min)
- 🔲 DeepLearning.AI short course (~90 min, optional)
- 🔲 Other two Anthropic docs as needed

### Concepts covered (out of 5 from "Develop test cases")

| # | Concept | Status | Notes |
|---|---|---|---|
| 1 | Eval is a hypothesis | ✓ deep | User pushed back on my "real claim vs. hypothesis" framing; corrected to **bounded evidence** — finite sample can never prove system quality, only narrow uncertainty |
| 2 | Source from reality, not invention | ✓ solid | Connected to user's synthetic `tickets_corpus.json` |
| 3 | Diversity beats volume | ✓ covered | 5 dimensions: length, tone, edge cases, topics, phrasing |
| 4 | Iterate the eval, not just the system | 🔜 pending | |
| 5 | Build incrementally | 🔜 pending | |

### Decisions NOT YET finalized
- **Eval target for Week 6 deliverables:**
  - **Option A** — Plan's example: extract `{action, owner, due_date}` from meeting notes (recommended)
  - **Option B** — Evaluate Week 5 RAG pipeline: did `search()` return the right ticket for each query?
  - User has not picked. **Ask on resume.**

## Week 6 deliverables (from the transition plan)

`llm-practice/evals/` directory containing:

```
evals/
  __init__.py
  golden_dataset.py    # 15-20 (input, expected_output) pairs
  judge.py             # LLM-as-judge, returns score + rationale
  run_eval.py          # CLI: run system against golden, score, report
  README.md            # what you measured, why, and what prompt change you made based on results
```

The plan calls out the README as **"the single most-quoted-from document in your interviews."**

## Stack and environment

Same as Week 5 — no changes:
- **Python + uv** at `llm-practice/pyproject.toml`
- **Postgres 16 + pgvector** in Docker, container `my-ai-eng-journey-db-1`, DB `rag`
- **Embeddings:** local Ollama `nomic-embed-text` (768 dims) — single source of truth in `week5/db.py` (`EMBEDDING_MODEL`, `DIMS=768`)
- **Chat:** OpenCode Go (kimi-k2) via `src/client.py`
- **`psycopg2` v2.x** with `register_vector(conn)` auto-called in `db.get_connection()`

## Week 5 surface area (context for Week 6)

If continuing on Option B (eval the RAG pipeline), these are the relevant pieces:

| File | Role |
|---|---|
| `llm-practice/src/week5/db.py` | `get_connection()`, `init_schema(conn)`, `check_drift(conn)`, `EMBEDDING_MODEL`, `DIMS=768` |
| `llm-practice/src/week5/query.py` | `embed_query()`, `search()`, `check_drift_warn()`, `run_query()` (argparse CLI) |
| `llm-practice/src/week5/ingest.py` | `load_corpus()`, `embed_tickets()`, `upsert_tickets()`, `main()`, `ingest_policy_chunks()` |
| `llm-practice/src/week5/chunking.py` | `chunk_fixed()`, `chunk_sentences()`, `chunk_recursive()` (used by `ingest_policy_chunks`) |
| `llm-practice/src/week5/benchmark.py` | `bake_off()`, `create_hnsw_index`, `create_ivfflat_index`, `bench_topk`, `recall_at_k`, `_measure_index_size` |
| `llm-practice/src/week5/policy.md` | 4375-char refund/shipping policy, 8 markdown headings |
| `llm-practice/src/midterm/tickets_corpus.json` | 12 synthetic tickets |

**Current DB state:** 40 rows in `tickets` (12 ticket embeddings + 28 policy-chunk embeddings, all `embedded_with='nomic-embed-text'`). HNSW and IVFFlat indexes both created and tested.

## Key concepts drilled cumulatively (across Week 5 and Week 6 so far)

### Week 5 — pgvector + RAG
- 3-layer model: extension on server + `register_vector(conn)` adapter + driver
- Drift detection via `embedded_with` column
- Positional pairing: `len(response.data) == len(batch)` + `record.index == i`
- Operator class ↔ operator: `vector_cosine_ops ↔ <=>`, `vector_l2_ops ↔ <->`, `vector_ip_ops ↔ <#>`
- HNSW (graph) vs IVFFlat (partitions): trade-off only matters at scale
- Chunking: fixed-size vs sentence-aware vs recursive hierarchical
- Heading-stickiness in `chunk_recursive`

### Python idioms
- `with` resource pattern vs `try/finally`
- mutable vs immutable types
- `TYPE_CHECKING` for type-only imports
- `time.perf_counter()` for benchmarking
- `statistics.median` for robust central tendency
- `cur` (no commit) vs `conn` (commits) — commit OUTSIDE `with` block
- DDL cannot use `%s` placeholders; f-string for parameterized DDL
- f-string format specs (`{i:03d}`)

### Week 6 — eval methodology (so far)
- **Bounded evidence, not proof** (the corrected framing of concept #1)
- **Source from reality** — synthetic data tends to be cleaner than reality
- **Diversity beats volume** — independent info per test, not correlated repeats
- Concepts 4 and 5 (iterate the eval, build incrementally) still pending

## User preferences

- Interactive tutoring session — concept deep dives on demand
- Reads code, asks questions, iterates with probes
- Tires easily — keep momentum, tight closeouts
- **IMPORTANT CHANGE from Week 5:** User explicitly flagged that they were not running scripts themselves — every run was delegated to me. New rule: **user runs, I review.** They want to see actual output, actual error messages, actual DB state.
- For commit work, delegate to `@fast-generic` (per project routing guidance)

## Next concrete actions when resuming

1. **Confirm Option A vs B for eval target** (first question on resume)
2. **Read "Define success" doc** (~30 min) before next concept session
3. Cover **concepts #4 and #5** (iterate the eval, build incrementally)
4. Scaffold `llm-practice/evals/` with the file structure above
5. Build `golden_dataset.py` first (the dataset shapes everything downstream)
6. Build `judge.py` (LLM-as-judge using OpenCode Go chat client)
7. Build `run_eval.py` (CLI to run system against golden, score, report)
8. Write `README.md` — the interview-quote-worthy artifact

## Suggested skills for the next agent

- `handoff` — to re-compact if a third laptop is added
- `verification-planning` — before implementing `run_eval.py` (the eval pipeline is non-trivial; worth a verification plan)
- `worktrees` — only if the user wants an isolated lane for the eval work (probably not needed; this is a single-developer repo)
- `oh-my-opencode-slim` — only if user requests tuning of agent behavior
- `simplify` — after the eval pipeline works, for cleanup pass on the code

## Sensitive information

None included. No API keys, no passwords, no PII. The repo uses local Ollama for embeddings and OpenCode Go (already configured) for chat — no secrets to redact.

## Reference

- Plan file: `ai-engineer-transition-plan.md` (in repo root)
- Week 6 section in the plan: search for "Week 6" or "evals" or "golden dataset"
- GitHub: https://github.com/frankielin2015/my-ai-eng-journey
- Anthropic docs to read next: https://platform.claude.com/docs/en/test-and-evaluate/define-success