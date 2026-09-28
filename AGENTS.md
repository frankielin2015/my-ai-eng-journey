# AGENTS.md — my-ai-eng-journey

Guidance for AI coding agents (Pi, Claude, Codex, etc.) working in this repository. Read this before making changes.

## What this repo is

A personal learning/workspace monorepo for an AI-engineer transition (see `ai-engineer-transition-plan.md` for the 16-week plan). It is **not** a production application — it contains deliberate practice code, handoffs, and notes. Keep that framing in mind: correctness and TDD discipline matter, but so do clear explanations and learning notes.

## Layout

- `ai-engineer-transition-plan.md` — master career plan (living document; decisions log explains why things are the way they are)
- `HANDOFF-*.md` — session-to-session handoff notes; read the most recent one before picking up work
- `llm-practice/` — LLM engineering practice (Python 3.14, `uv`, structured outputs, evals, RAG/pgvector, midterm project). Uses `openai` SDK with `base_url` pointing at Ollama (OpenAI-compatible). Evals run via `promptfooconfig.yaml` in this folder.
- `python-practice/` — completed Python TDD gym (67/67 green). Mostly historical; don't refactor for fun.
- `docker-compose.yml` — pgvector (pg16) dev database for RAG work, db `rag`, user/pass `postgres`.
- `skills-lock.json` — pinned external skills (mattpocock/skills).

## Environment & commands

- Python is managed with **`uv`** (each practice folder has its own `pyproject.toml` + `uv.lock`). Run everything with `uv run <cmd>` from inside the folder.
- LLM exercises use `openai` SDK against Ollama Cloud via `base_url` override; API keys come from `.env` (`python-dotenv`). Never hardcode keys.
- Database: `docker compose up -d db` from repo root when pgvector is needed.
- Tests: `uv run pytest -v` (per-project).
- Commit with concise, conventional messages (feat/fix/docs/chore).

## Working rules for agents

1. **TDD-first in practice folders.** When implementing exercises, keep the red→green loop: run the matching test module, implement, re-run. Don't rewrite the provided test suites unless explicitly asked.
2. **Preserve handoff integrity.** `HANDOFF-*.md` files are the memory across sessions. When finishing meaningful work, update or create a handoff note instead of relying on chat history.
3. **Don't touch the decisions log history.** Append to the plan's Decisions Log with rationale; never rewrite old entries.
4. **Explain while building.** This is a learning repo — prefer code with brief explanatory comments and honest notes in handoffs over silent "magic fixes".
5. **Keep provider portability.** LLM code should stay OpenAI-SDK-shaped (portable across Ollama/OpenRouter/etc.). Anthropic SDK usage is read-only/conceptual unless the user says otherwise.
6. **Secrets stay in `.env`**; if a conversation/export contains credentials, warn before `/share` or `/export`.
7. Ask before: adding new dependencies, deleting or renaming files, restructuring folder layout, or git push.

## Conventions

- Python: modern 3.14 style, type hints, `pathlib`, no default mutable args.
- Docs: Markdown, always Update handoffs using "Where we left off / What's next" structure.
- Source of truth: the plan doc > handoff notes > chat context.
