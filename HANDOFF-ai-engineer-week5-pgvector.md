# HANDOFF — AI Engineer Journey (Week 5: pgvector + RAG)

**Date:** 2026-09-09
**Status:** Week 4 COMPLETE and committed. Next session opens Week 5.

## How to use this document

This is a compensating summary of one conversation. The authoritative artifacts
live elsewhere — read them first, then use this doc for the operational context
matters they don't capture.

**Read in this order:**
1. `/Users/xiaofalin/WorkSpace/my-ai-eng-journey/ai-engineer-transition-plan.md` (canonical 16-week plan; Week 4 now marked complete, Week 5 materials already link-verified and substituted)
2. `/Users/xiaofalin/WorkSpace/my-ai-eng-journey/llm-practice/docs/wk4-demo-run.md` (Week 4 deliverable evidence)
3. `/Users/xiaofalin/WorkSpace/my-ai-eng-journey/llm-practice/src/week4/semantic_search.py` (Week 4 code)
4. `/Users/xiaofalin/WorkSpace/my-ai-eng-journey/llm-practice/docs/wk3-handoff.md` (older open threads, some still pending — see below)

Git logs (do not re-summarize here):
- Parent repo `my-ai-eng-journey`: `e07e376` (Week 4 complete), `77171de`, `0547dc7`, `f7e8567`, `eb3c790`
- `llm-practice` repo: `7609d16` (Week 4 deliverable)

## Who the user is / how to work with them

- Staff-level SWE (7y TS/Java/React, SRE/platform background), learning Python + AI engineering. Learner mode, not pair-programmer mode.
- **Wants:** step-by-step mentoring, concepts taught with plain language and concrete numeric examples, one step at a time with comprehension checks before advancing.
- **Writes all the real code himself.** The proven pattern is: agent scaffolds a skeleton with TODOs, user implements them one at a time, agent reviews each with line-level feedback. This worked extremely well for Week 3 and Week 4.
- **Dislikes:** verbosity, unrequested detail, being referenced to files/functions that don't exist yet. Keep answers tight. Ask before assuming.
- **Strong signal he gives:** honest "I don't understand" at the exact point of confusion. Treat this as gold, not failure. He has explicitly asked to be corrected and to be told when he is off-rails.
- Do **not** fabricate eval/run results. He values observed evidence (the plan's culture). Only record what was actually run.

## Environment / how to run things

- Workspace root: `/Users/xiaofalin/WorkSpace/my-ai-eng-journey`
- Python work lives in `/Users/xiaofalin/WorkSpace/my-ai-eng-journey/llm-practice`
- **Run prefix (required — Rosetta workaround):**
  `cd /Users/xiaofalin/WorkSpace/my-ai-eng-journey/llm-practice && /usr/bin/arch -arm64 uv run python <script>`
- `promptfoo` is installed globally (Node v24 via nvm) — run it natively, no npx.
- **Secrets:** `OLLAMA_API_KEY` lives in `llm-practice/.env` (do not print it). User does not want to export it into the shell; use `--env-file .env` where relevant.

## Provider architecture (important — discovered this session)

- **Chat:** Ollama Cloud via `https://ollama.com/v1`, key from `.env`. Models seen: `kimi-k3:cloud`, `gpt-oss:20b`, `deepseek-v4-flash:cloud`. Factory: `make_client()` in `llm-practice/src/client.py`.
- **Embeddings:** Ollama Cloud has **no** `/v1/embeddings` endpoint (probe-verified: route 404, chat routes fine). Embeddings run on **local Ollama** at `http://localhost:11434/v1` (any non-empty key works). Model: `nomic-embed-text` (768 dims). Factory: `make_embedder()` in the same `client.py`. Local Ollama must be running (`ollama serve` or the app).
- Two clients, one SDK. This decision is recorded in the plan under Week 4 materials (dated stack note). Do not silently change it.

## What was accomplished (this conversation)

- **Week 3 fully closed** (lab, promptfoo eval, CHANGELOG, essay, commits) — see git log and `llm-practice/prompts/CHANGELOG.md`. Key findings: promptfoo v1 0/14 vs v2 6/14; kimi ~50% fence compliance, `gpt-oss:20b` ignores output contracts; "structure teaches structure."
- **Week 4 fully closed:**
  - Materials walked (Pinecone article dropped as unhelpful; StatQuest + IBM video + cookbook completed). Cookbook taught interactively, section by section.
  - Dead links during Week 4/5 material review were verified and substituted (librarian research): two James Briggs YouTube videos removed; OpenAI Cookbook pages removed in their site migration. Plan updated and committed (`f7e8567`, `0547dc7`).
  - Built `semantic_search.py` together: collect (`load_corpus`, comprehension), batch embed (both truncation + pairing asserts), store JSON, hand-written cosine similarity, pure `search()` with top-k.
  - Demo: `"function wrapper"` → decorator cheatsheet (0.537) with **no keyword overlap** — semantic match proven. `"pizza recipe"` → flat low scores (no-match shape).
  - Success test passed verbally: same-model rule explained (own-map per model; mixing = silent garbage, no error).
- Cognitive takeaway the user named himself: reading materials left concepts foggy; writing the code made them click. Reuse this — push to the smallest buildable version when material fogs up, then re-read.

## Next session: Week 5 (pgvector + RAG)

Week 5 materials in the plan are already corrected/substituted — open the plan, don't redo discovery. Sequence:
1. "Why pgvector" decision-basis reading: Pinecone *What is a Vector Database?* + pgvector README (both link-verified).
2. Supabase pgvector guide (substitute for the deleted OpenAI cookbook notebook) — run the embed→store→index→query flow with **local Postgres in Docker**, not Supabase cloud.
3. Build: RAG ingestion + query script over a corpus; pgvector in Docker; commit with README noting chunking strategy, embedding model, top-k, and an example query + retrieved chunks.

Teaching angle to preserve: the Week 4 brute-force loop is the **baseline** — Week 5 shows what pgvector's ANN index trades away (recall for speed / HNSW vs IVFFlat). The user's Postgres background is the differentiator; connect to it.

## Open threads (carried, low priority)

From `llm-practice/docs/wk3-handoff.md`:
- `src/week2/ex2_sentiment_extractor.py` — `MODEL` is still `"gpt-oss:20b"` (was never reverted).
- `openai` SDK pin is looser than desired (`>=3.3.1`); consider pinning.

Neither blocks Week 5.

## Suggested skills

Next agent should call the Skill tool for:
- `oh-my-opencode-slim` — the user runs oh-my-opencode-slim (built on oh-my-opencode); use it for any config/agent/prompt tuning or when workflow friction suggests a config improvement.
- `verification-planning` — Week 5 is a non-trivial build (Docker + Postgres + pgvector + RAG ingestion); plan the evidence path before implementing.
- `simplify` — available if the Week 5 script accumulates clutter; use after behavior is understood.
