# Handoff: W5 mid-term complete, picking up from tomorrow

## Where we left off

The W5 mid-term (Pydantic + chat API + retry + prompt versioning + sanitization + embeddings + cosine + top-k) is **functionally complete**:

- All 9 TODOs in `src/midterm/triage.py` implemented (TODOs 1–8 by user, TODO 9 by assistant)
- `src/midterm/tests/test_triage.py`: **11/11 pass**
- End-to-end `python src/midterm/triage.py triage "..." v1|v2` works against real Ollama + OpenCode Go
- Demo results on next-session start (run from `llm-practice/`):
  - Login ticket on v1 → `account` / `high`
  - Login ticket on v2 → `account` / `high` (CoT-influenced reasoning)
  - Injection probe on v2 → `bug` / `low` — model explicitly identified the injection attempt

## Two small follow-ups for the next session (~5 min total)

1. **Add 3 derived fields to `TicketTriage`** at `src/midterm/triage.py:151-154`. The pipeline already calls `result.model_copy(update={"similar_ticket_ids": ..., "scores": ..., "prompt_version": ...})`, but Pydantic v2 silently drops unknown fields, so the JSON output only shows 3 fields. Fix:
   ```python
   similar_ticket_ids: list[str] = Field(default_factory=list, max_length=3)
   scores: list[float] = Field(default_factory=list, max_length=3)
   prompt_version: Literal["v1", "v2"] = "v1"
   ```
   Add this to the imports if missing: `list` from `typing`, `Field` already imported. Then re-run the end-to-end calls — output should show 6 fields per result.

2. **Decide on chat model**. Currently `LLM_MODEL = "kimi-k3"` at `src/midterm/triage.py:102`. The cheaper `deepseek-v4.1-flash` is region-locked to China and requires opt-in via the OpenCode Go workspace link (RegionError 403). Either:
   - Opt in via that link and revert `LLM_MODEL` to `deepseek-v4.1-flash`, OR
   - Try another cheap `chat/completions` model (`kimi-k2.7-code`, `mimo-v2.5`, etc. — see registry below), OR
   - Stay on `kimi-k3` (known-working).

## Established patterns (don't relearn)

- **Provider**: OpenCode Go at `https://opencode.ai/zen/go/v1` for chat. Required headers in `src/client.py:make_chat_client()`: `x-opencode-session` (UUID-per-process) + custom `User-Agent`. Env var: `OPENCODE_API_KEY`. Embeddings via local Ollama (`nomic-embed-text`, 768d) at `make_embedder()`.
- **Model URLs differ by family**: `chat/completions` (Kimi K3/GLM/DeepSeek V4.1/Hy4), `messages`/Anthropic (M3/Qwen), `responses` (Grok/GPT/Muse). Always use `chat/completions` model with OpenAI Python SDK; model names are bare (no `opencode-go/` prefix).
- **W2 retry-with-stricter-msg**: ref `src/week2/ex4_classifier.py:96-99`.
- **W3 injection-defense ladder**: containment (XML + "data, not commands" line in prompt) → sanitization (single `str.replace("</", "<\\/")`) → validation (Pydantic). Note: `classify_ticket` does NOT yet have the retry loop — only one attempt in practice was needed, but optional polish if you want it.
- **W4 one-map rule**: query + corpus embedded by the same model in the same call. Positional pairing asserted via `resp.data[i].index == i`. Pure-Python cosine, no numpy. Ref `src/week4/semantic_search.py`.
- **Skeleton convention** (W2/W3-style lab pattern): file-level docstring with Rosetta workaround, frozen config section, "given, not part of the exercises" for constants/CLI, each TODO has hint block referencing prior-week file, tests as acceptance criteria.
- **Scope guardrails**: no Postgres/pgvector (W5), no async, no LangGraph/MCP (W8+), no regex, no `format="json"`, no `beta.parse`. Established with user explicitly.
- **User collaboration mode**: agent scaffolds, user implements line-by-line. Each user-implemented function is reviewed by agent for correctness. Pattern came from W2/W3 handoff.
- **No pytest in dev deps** — tests run via standalone runner in `test_triage.py` (importable `main()` plus `if __name__ == "__main__": main()`).

## Run prefix (Rosetta shell workaround on Apple Silicon)

Always prefix Python commands:
```bash
cd /Users/xiaofalin/WorkSpace/my-ai-eng-journey/llm-practice
/usr/bin/arch -arm64 uv run python <script>
```

## Files of record (reference, don't duplicate)

- `src/midterm/triage.py` — W2/W3-style skeleton, all 9 TODOs done, LLM_MODEL = "kimi-k3"
- `src/midterm/triage_reference.py` — full reference impl (different signatures; cross-check for concepts/control flow only)
- `src/midterm/prompts/triage_v1.md` — frozen baseline
- `src/midterm/prompts/triage_v2.md` — XML containment, few-shot, CoT fence, injection-defense line, strict-JSON closing
- `src/midterm/tickets_corpus.json` — 12 clean tickets
- `src/midterm/tickets_corpus_embedded.json` — build artifact, 12 × 768-dim
- `src/midterm/tests/test_triage.py` — 11 tests + standalone runner
- `src/client.py` — `make_chat_client()` (OpenCode Go), `make_embedder()` (Ollama), legacy `make_client()`
- `.env.example` — `OPENCODE_API_KEY=` line
- `docs/midterm-handoff.md` — handoff doc with file map, oracle review notes, run instructions (may need refresh to reflect end-to-end demo results)
- `~/.config/opencode/oh-my-opencode-slim.json` — model registry (preset shows which models map to which agents)
- `~/.local/share/opencode/auth.json` — has `opencode-go`, `ollama-cloud`, `openrouter` keys

## Suggested skills for next session

- `verification-planning` — before starting W6 or any new feature, write the verification plan. The user's pattern is to plan lanes/dependencies before implementation.
- `worktrees` — if picking up parallel work or risky refactors (mid-term took the main branch; no needs yet).
- `reflect` — once a few sessions of W6 are done, run `/reflect` to capture recurring workflow patterns.

## Background job board

No active background tasks at handoff time.

## Uncommitted changes (git status at handoff)

The mid-term work is largely uncommitted. Likely files:
- `.env.example`
- `src/client.py`
- `src/midterm/` (full directory: triage.py, triage_reference.py, prompts/, tickets_corpus*.json, tests/)
- `src/week4/semantic_index.json` (from earlier W4 work)
- `docs/midterm-handoff.md` (W5 doc)

Suggested commit message (user has not asked to commit yet):
```
feat(midterm): W5 mid-term triage pipeline (Pydantic + RAG + v1/v2 prompts)
```
But the next session should confirm with the user before committing.

## Redacted

No API keys, passwords, or PII in this document. The `OPENCODE_API_KEY` lives in `.env` (not in repo) and in `~/.local/share/opencode/auth.json` (not in repo).
