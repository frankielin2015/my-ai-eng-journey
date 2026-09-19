# Week 3 Handoff — AI Engineer Transition (Xiaofa)

_Dropped off: Thursday evening, Week 3 (plan week runs Wed–Sun; ~2 hrs/day budget)_
_Next session should start by reading this file + checking the plan file's Week 3 section._

## Project context (stable facts)

- **Journey**: 16-week AI-engineer transition plan. Canonical plan file:
  `ai-engineer-transition-plan.md` (repo root). Weeks 1–2 complete; **currently in Week 3**.
- **Repo**: `llm-practice/` (git initialized, `master`). Parent dir `my-ai-eng-journey/` has its own repo.
- **LLM stack**: Ollama Cloud via official `openai` SDK, `base_url="https://ollama.com/v1"`,
  `OLLAMA_API_KEY` env var. Run prefix (Rosetta shell workaround):
  `cd /Users/xiaofalin/WorkSpace/my-ai-eng-journey/llm-practice && /usr/bin/arch -arm64 uv run python <script>`
- **Models used**: `kimi-k3:cloud` (primary), `gpt-oss:20b` (experiment), `deepseek-v4-flash:cloud`.
  Client factory: `src/client.py` `make_client()`.
- **Week 2 core finding** (context for Week 3 story): "OpenAI-compatible" = wire format only.
  Structured outputs (`response_format=PydanticModel`) are **silently ignored** by Ollama Cloud →
  markdown prose → Pydantic `ValidationError`. Injection probe was *executed* by `gpt-oss:20b`.
  Defensive pattern: prompt constraint → schema hints → Pydantic validation + retry → graceful None.

## Week 3 state

### Materials — ALL DONE (with substitutions)
1. Prompt engineering overview ✅ (it's a TOC, not content)
2. Best-practices page ✅ — XML tags / multishot / CoT sections covered (plus a full video course:
   "Prompt Engineering Full Course" https://www.youtube.com/watch?v=2BpCk4d2Cc0)
3. Chain prompts / long-context — SKIPPED by design (Building Effective Agents covers chaining better)
4. Interactive tutorial — **SKIPPED permanently** (requires paid Anthropic API key; free credits
   discontinued; all its techniques already covered twice)
5. Building Effective Agents ✅ (materials list per user: 1,2,3,5,7 done)
6. PromptFoo cookbook — **404** (repo restructure); replaced by promptfoo's own docs
   (provider support verified: `ollama:chat:<model>` + `OLLAMA_BASE_URL` + `OLLAMA_API_KEY`;
   fallback = openai-compatible provider with `config.baseUrl: https://ollama.com/v1`)
7. Field guide role/02-skills.md + 03-responsibilities.md ✅

### Deliverables
1. **`llm-practice/prompts/`** — DONE except one CHANGELOG edit (below)
   - `sentiment_v1.md` — frozen baseline. Zero-shot, no techniques. Placeholder `{{user_text}}`.
   - `sentiment_v2.md` — complete. XML tags (`<instructions>/<examples>/<review>`), 4 schema-exact
     multishot examples (positive anchor / mixed boundary / neutral+empty topics / negation trap),
     injection-defense line inside `<instructions>`, CoT directive as the LAST block
     (`Before answering, reason step by step inside <thinking> tags: 1 quote phrases → 2 check
     negation/expectation flips → 3 decide; After </thinking>, output ONLY the JSON object`).
     Key mechanism taught: the model (not the prompt) emits the `<thinking>` fence; extraction via
     `raw.split("</thinking>", 1)[-1].strip()`.
   - `CHANGELOG.md` — still contains scaffold TODO entries; **TODO: rewrite with real entries**
     (v1 done + "mix" enum lesson; schema migration entry; v2 done + fence/extraction note;
     eval-result slot for Saturday)
2. **promptfoo config** — NOT STARTED (Saturday item; config template was already drafted in
   conversation, see "Next steps" below)

### Code changes made (already on disk)
- `src/week2/ex2_sentiment_extractor.py`: schema widened —
  `Literal["positive","negative","neutral"]` → `Literal["positive","negative","mixed","neutral"]`
  (doc comment + field). **Schema migration story: prompt work exposed taxonomy gap; recorded in CHANGELOG.**
- **UNCOMMITTED**. Suggested commit:
  `git add prompts/ src/week2/ex2_sentiment_extractor.py && git commit -m "Week 3: versioned sentiment prompts v1/v2 + schema migration (+mixed)"`

## Key teaching decisions & lessons (don't re-explain, just reuse vocabulary)

- Placeholder contract: `{{user_text}}` in `.md` files, rendered via `str.replace()` (NOT
  `str.format()` — JSON braces break it). f-strings only for inline prompts; v1–v4 ex-scripts use
  message-dict constants, no interpolation.
- Prompt-versioning-as-schema-migrations analogy = Week 3 success test; war stories: "mix" enum
  mismatch caught in review; `+mixed` migration; never edit a released version.
- Multishot examples are output templates — model copies them literally (a deliberately malformed
  example got pasted once; fixed).
- Injection analogy ladder: SQL/XSS ↔ prompt injection; defenses = containment (tags + ignore line,
  weak) → sanitization (`</` escape, strong/structural) → validation (Pydantic, guaranteed).
  No "parameterized queries" equivalent for LLMs — mitigate in depth.
- Adversarial probes designed for the lab: seeded `<thinking>`, forged `</review>`, fake
  `</thinking>` (breaks extraction).

## Next steps (in order)

1. **Commit current work** (command above) if not done yet.
2. **Lab: `llm-practice/src/week3/lab_sentiment.py`** (~45 min) — scaffold was fully drafted in the
   last conversation turn: Part A `render(review, sanitize)` with `</` → `<\/` sanitize option;
   Part B call → `split("</thinking>")` → `json.loads` → `SentimentResult.model_validate`;
   Part C probes dict {innocent, seeded, escape, breaker} × sanitize on/off × models
   (kimi-k3:cloud, then gpt-oss:20b). Record per-probe results.
3. **promptfoo eval** (Sat) — `promptfooconfig.yaml` with `prompts: [file://sentiment_v1.md,
   file://sentiment_v2.md]`, Ollama provider (native `ollama:chat:` first; fallback openai-compatible
   `baseUrl: https://ollama.com/v1`), tests incl. `is-json` + sentiment asserts; record v1-vs-v2
   delta in CHANGELOG. Watch for: v2 raw output includes `<thinking>` fence → may need a transform
   before `is-json` (legitimate finding if so).
4. **Success test** (Sun) — say the schema-migrations analogy aloud with the three war stories;
   write `docs/wk3-prompt-versioning.md`; update plan file: mark Week 3 done + record material
   substitutions (4 skipped/key, 6 replaced); final commit.

## Open threads (minor)

- Plan-file path inconsistency: plan says `llm-experiments/prompts/` but reality is
  `llm-practice/prompts/` — fix when updating plan file.
- `ex2` MODEL still `"gpt-oss:20b"` from experiments (not reverted).
- Suggested-but-pending: pin `openai` SDK tighter than `>=3.3.1` for beta-API safety.