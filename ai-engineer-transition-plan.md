# AI Engineer Transition Plan — Monolith

**Owner:** Xiaofa — Staff Software Engineer, Walmart Global Tech (~7 YOE)
**Goal:** Transition into Agentic / Applied AI Engineering at a Tier-1 or Tier-2 company; keep internal Walmart opportunities as parallel leverage
**Time budget:** 7–8 hrs/week, 16 weeks
**Started:** 2026-08-23
**Target completion:** ~2026-12-13 (16 weeks from start)
**Status:** Living document — update as you progress
**Revised:** 2026-08-24 (v2 — see Decisions Log #7–8) — fixed Week 10–11 overload between Project 2 build and interview prep, added behavioral story-bank prep, moved first applications earlier (Week 8 instead of Week 13) via a decoupled schedule. Total plan length unchanged at 16 weeks.

---

## Decisions Log (why this plan looks the way it does)

Locked in on 2026-08-23 after iterating with Claude:

1. **Language**: Python-first portfolio. Confirmed 2026-08-24 — TS/JS is the actual career strength (7 years of daily use), but the field guide's job-market data shows Python as the dominant AI-eng stack, and LeetCode-style rounds are more naturally done in Python. Deliberate tradeoff: give up the language-speed advantage in exchange for market/interview alignment. TS experience still comes through in the narrative (platform/tooling background), just not in the portfolio code itself.
2. **Portfolio shape**: Two projects — **Agent Observability Dashboard** and **Delivery-Ops Triage Agent** — inherited from the prior Claude roadmap, kept unchanged. Both wire together into one composable system.
3. **Targets**: External-first (Tier 1 = Anthropic / OpenAI / Google DeepMind; Tier 2 = LangChain / Chroma / Pinecone / Weights & Biases / Langfuse / Cohere / Scale AI; Tier 3 = Meta / Microsoft / Amazon / Nvidia AI-platform teams). Internal Walmart agentic-AI platforms kept warm in parallel as leverage.
4. **Pace**: 7–8 hrs/week. Plan takes 16 weeks; if a week gets blown up by work, shift forward — don't cram.
5. **Phase 0 scope**: Python foundations are treated as a tracked phase (gym refresh + async Python + a 1-hr FastAPI hello-world). The full Python TDD gym in `python-practice/` is already complete (67/67 green). FastAPI is NOT a deep detour — Pydantic understanding comes primarily via structured outputs in Week 2.
6. **Evals are first-class**: Week 6 is dedicated to evals (the field guide flags this as the #1 gap for backend engineers). Basic ML (PyTorch, fine-tuning) is deferred — it does not differentiate inside a 16-week window for applied/agentic roles.
7. **Job-search timing (revised 2026-08-24)**: Original plan crammed resume rewrite + question banks into Weeks 10–11, the exact weeks Project 2 needs full focus — one of the two would've suffered. Fixed by decoupling: a light narrative/resume pass happens right after Project 1 ships (Week 7), enabling **low-volume applications starting Week 8** (Tier 3 postings, treated as calibration/practice, not top targets). Weeks 10–11 become **protected build time** — Project 2 only, nothing else competing. Full resume polish + behavioral story bank move to Week 12, after both projects are shipped. Technical question bank + AI system design prep + ramp to full application volume (5–8/week, Tier 1 first) happens Week 13. Internal Walmart recon (low-effort, 2–3 chats) happens Week 9, running alongside Project 2 build since it costs little time.
8. **Behavioral prep added**: The original plan had no space for STAR-method story prep. Tier-1 labs weight behavioral rounds heavily, and technically strong candidates often lose ground here specifically because they didn't prepare concrete stories in advance. Added as a dedicated deliverable in Week 12, alongside the resume rewrite.
9. **Phase 0 scope narrowed further (revised 2026-08-24)**: FastAPI hello-world removed from Week 1 entirely and deferred to Week 7 if useful for Project 1's dashboard endpoint. Rationale: Pydantic arrives in Week 2 via structured outputs (the load-bearing destination), and a FastAPI claim only matters if it's true because a real service shipped — not because a tutorial was completed. Phase 0 wraps after async/await + lint setup.
10. **LLM provider for exercises (added 2026-08-24)**: Ollama Cloud (hosted provider, OpenAI-protocol compatible — same shape as OpenRouter) is the default backend for exercises, accessed via the official `openai` Python SDK with a `base_url` override. Anthropic SDK exercises in Week 2 are concepts + read-only by default (no paid API key), with Anthropic's $5 free trial credit as an option for hands-on. Rationale: learn the two dominant SDKs (OpenAI + Anthropic) without paying for either; `openai`-SDK-shaped code is portable across providers (Ollama, OpenRouter, Together, Groq, vLLM, OpenAI itself) so this choice doesn't narrow future options.

Supersedes `agentic-ai-career-roadmap.md` (kept for history).

---

## The Narrative (internalize this — you will repeat it everywhere)

> "Build platforms and tools that other engineers depend on, with reliability baked in. I'm extending that same skill to agentic AI systems — a domain that badly needs more production discipline than it currently has."

Every project README, every cover letter, every interview answer should be *concrete evidence* for this sentence.

---

## Target Companies

### Tier 1 — AI labs (primary focus)
- **Anthropic** — Applied AI Engineer, Forward Deployed Engineer, Agents Platform
- **OpenAI** — Forward Deployed Engineer, Solutions Engineer, Applied Engineer
- **Google DeepMind / Gemini Applied** — AI Engineer, Applied AI, Agents

### Tier 2 — AI infrastructure / tooling
- LangChain, Chroma, Pinecone, Weights & Biases, Langfuse, Cohere, Scale AI

### Tier 3 — Large-tech AI platform teams
- Meta GenAI, Microsoft Copilot Platform, Amazon AGI, Nvidia NeMo

### Parallel internal track — Walmart Global Tech
- Agentic AI / AI platform teams — keep warm via informational chats starting Week 12. Acts as fallback + external-offer negotiation leverage.

---

## Phase 0 — Python Foundations Wrap-Up (Week 1, ~4–5 hrs)

The full TDD gym is already done (67/67 green in `python-practice/`). This week is the *wrap-up* — close the gaps that actually matter for AI work: async Python, plus a 1-hour FastAPI hello-world.

### Learning objectives
- Read async Python (LangGraph, OpenAI/Anthropic SDKs) without mentally translating
- Have a working lint/typecheck habit (ruff + pyright) before project work

### Materials (do these, in order)
1. **Gym refresh** (30 min) — `cd python-practice/ && uv run pytest`. Expect 67/67 green. Re-read `SESSION_NOTES.md` sections "Concepts covered so far" and "Open review note in ex05". *(Completed — reviewed Python fundamentals 2026-08-24.)*
2. **Async Python — Corey Schafer series** (90 min, watch at 1.5x) — https://www.youtube.com/playlist?list=PL-osiE80TeTsW6VCPUiN9131_VKHFt2D4
3. **Async IO walkthrough — Real Python** (45 min, skim code samples) — https://realpython.com/async-io-python/
4. **Motivation read — Anthropic Engineering** (10 min) — https://claude.com/blog/writing-code-with-claude
5. **(Optional) Lint/typecheck setup** (30 min) — Add `ruff` + `pyright` to `pyproject.toml`. Configure in CI later.

**Deferred:** FastAPI hello-world — originally a 1-hour item here, now deferred to Week 7 if useful for Project 1's dashboard endpoint. Pydantic arrives in Week 2 via structured outputs anyway, so learning FastAPI in isolation isn't load-bearing at this stage. Phase 0 is considered wrapped once items 1–4 above are done.

### Deliverables
- None required for Phase 0 itself. The `fastapi-hello/` repo is deferred to Week 7 if/when actually needed by Project 1.

### Success test
Can I read async LangGraph / OpenAI SDK source on GitHub without translating mentally?

---

## Phase 1 — LLM Foundations (Weeks 2–4, 7–8 hrs/week)

Build the vocabulary and mechanical fluency: OpenAI + Anthropic SDKs, structured outputs, function calling, prompt engineering + versioning, embeddings.

### Week 2 — OpenAI + Anthropic SDKs, structured outputs, function calling ✅ COMPLETE

**Status:** Completed Aug 29, 2026 — all deliverables built and tested against Ollama Cloud.

**Pre-step: provider setup (~15 min).** You don't need to pay for OpenAI or Anthropic API access. Use **Ollama Cloud** (a hosted provider like OpenRouter, not a local model) as your primary backend — it implements the OpenAI REST protocol, which means the official `openai` Python SDK works against it just by overriding `base_url`:

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://ollama.com/v1",
    api_key="<your Ollama Cloud key>",
)

response = client.chat.completions.create(
    model="kimi-k3:cloud",  # or gpt-oss:20b, deepseek-v4-flash:preview
    messages=[{"role": "user", "content": "Hello"}],
)
```

Test it with one small script before starting the Week 2 materials so SDK issues don't eat into study time.

**Anthropic SDK note:** Anthropic's API is *not* OpenAI-compatible. Items 4–6 on Anthropic's `messages` and `tool_use` shape: do them as **concepts + read-only** (read the docs/notebooks without running code) OR sign up for Anthropic's free $5 trial credit (no credit card required) — enough to run all Anthropic examples in this plan. Either way works; Anthropic-tier interviewers will care that you understand the API shape and can read their SDK source, not that you maxed out credits.

**Key findings from Ollama Cloud testing** (documented in `llm-practice/docs/wk2-ollama-quirks.md`):
- `response_format=PydanticModel` is **silently ignored** — model generates prose, not JSON. Pydantic catches it via `ValidationError`.
- `.refusal` field is **not populated** — models decline in prose or execute injections (varies by model: kimi-k3 refused, gpt-oss executed).
- `maxLength` in JSON Schema is **not enforced** by the model — it's a Pydantic-level check only.
- **Retry with explicit prompt constraint** is the production pattern: "Keep summary under 100 characters" prevents most failures; `model_validate` + retry catches the rest.

**Caveats of Ollama Cloud vs frontier models** (worth noting in project READMEs later — interviewers will ask):
- Structured outputs work via `format="json"` + Pydantic, but with weaker "strict" guarantees than OpenAI's `response_format: json_schema`.
- Tool-calling accuracy varies by open model. For learning the pattern that's fine; for Project 2's reliability story, acknowledge in the README that local/open models are for iteration speed and a frontier model would be the production choice.
- **Ollama Cloud ≠ OpenAI behavior**: wire format compatible, schema enforcement absent. Client-side validation is the only portable guarantee.

**Materials covered:**
1. OpenAI — *Structured Outputs guide* (45 min) — https://platform.openai.com/docs/guides/structured-outputs
2. OpenAI — *Function Calling guide* (45 min) — https://platform.openai.com/docs/guides/function-calling
3. OpenAI Cookbook — *How to call functions with chat models* (60 min, run the notebook against Ollama Cloud) — https://cookbook.openai.com/examples/how_to_call_functions_with_chat_models
4. Anthropic — *Messages API overview* (30 min, read-only) — https://docs.anthropic.com/en/api/messages
5. Anthropic — *Tool use with Claude* (60 min, including code examples — read/run if you signed up for trial credit) — https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview
6. Anthropic Cookbook — *Tool use with Pydantic* (60 min, read-only or run with trial credit) — https://github.com/anthropics/anthropic-cookbook/blob/main/tool_use/tool_use_with_pydantic.ipynb
7. OpenAI Cookbook — *Structured outputs intro* (45 min) — https://cookbook.openai.com/examples/structured_outputs_intro

**Deliverables completed:**
- ✅ `llm-practice/src/week2/ex1_function_calling.py` — function calling loop (tool schema → LLM call → execute → respond)
- ✅ `llm-practice/src/week2/ex2_sentiment_extractor.py` — structured outputs + Pydantic + Ollama quirks (ValidationError handling)
- ✅ `llm-practice/src/week2/ex3_json_transformer.py` — JSON-to-JSON transformer with function calling
- ✅ `llm-practice/src/week2/ex4_classifier.py` — support ticket classifier with routing + retry logic
- ✅ `llm-practice/docs/wk2-ollama-quirks.md` — README note on OpenAI vs Ollama Cloud differences

**Success test:** ✅ Can explain the difference between JSON mode and strict structured outputs, when function calling beats parsing, and why client-side validation is non-negotiable when crossing API providers.

---

### Week 3 — Prompt engineering + prompt versioning ✅ COMPLETE

**Status:** Completed Sep 5, 2026 — versioned prompts, adversarial lab, and promptfoo eval all shipped.

**Material substitutions (recorded):**
1. Prompt engineering overview ✅ (it's a TOC, not content)
2. Best-practices page ✅ — XML tags / multishot / CoT covered (+ a full video course: "Prompt Engineering Full Course" https://www.youtube.com/watch?v=2BpCk4d2Cc0)
3. Chain prompts / long-context — SKIPPED by design (Building Effective Agents covers chaining better)
4. Interactive tutorial — **SKIPPED permanently** (requires paid Anthropic API key; free credits discontinued; techniques covered elsewhere)
5. Building Effective Agents ✅ (THE canonical read)
6. PromptFoo cookbook — **404** (repo restructure); replaced by promptfoo's own docs (openai-compatible provider with `apiBaseUrl: https://ollama.com/v1` works against Ollama Cloud)
7. Field guide role/02-skills.md + 03-responsibilities.md ✅

**Deliverables completed:**
- ✅ `llm-practice/prompts/` — `sentiment_v1.md` (frozen zero-shot baseline) + `sentiment_v2.md` (XML containment, multishot, CoT fence) + `CHANGELOG.md` documenting what/why/measured effect
- ✅ Schema migration recorded: `+mixed` enum widening in `src/week2/ex2_sentiment_extractor.py` (taxonomy gap exposed by v2 review)
- ✅ `llm-practice/src/week3/lab_sentiment.py` — adversarial probe matrix ({innocent, seeded, escape, breaker} × sanitize × {kimi-k3, gpt-oss}); defense-in-depth ladder verified empirically
- ✅ `llm-practice/promptfooconfig.yaml` + `promptfoo_transform.py` — v1 vs v2 eval on Ollama Cloud
- ✅ `llm-practice/docs/wk3-prompt-versioning.md` — schema-migrations essay (success test)

**Key findings (full detail in `llm-practice/prompts/CHANGELOG.md`):**
- **v1: 0/14 vs v2: 6/14** on promptfoo (7 tests × 2 models per prompt) — instruction ≠ contract; structure teaches structure (multishot examples = output templates)
- Output-format compliance is model-dependent: gpt-oss:20b emits native `Thinking:` prose regardless of prompt contract (consistent with wk2 injection execution); kimi-k3:cloud complies with v2 structure
- Injection defense ladder verified: sanitization (`</` escape) neutralizes forged closing tags; `[-1]` extraction survives fake fences; format validation cannot detect judgment contamination (Pydantic validates shape, not provenance)
- Evals must discriminate: confounded probe (seed agreed with true sentiment) → ambiguous result; contradictory seed → real measurement

**Success test:** ✅ Explain prompt versioning as analogous to schema migrations — same discipline, different artifact (see `docs/wk3-prompt-versioning.md`).

---

### Week 4 — Embeddings + semantic similarity

**Materials:** *(Revised 2026-09-06 — original James Briggs videos removed from YouTube; substitutions verified live.)*
1. Pinecone — *What are Vector Embeddings?* (25–30 min, the canonical written intro) — https://www.pinecone.io/learn/vector-embeddings/
2. StatQuest — *Word Embedding and Word2Vec, Clearly Explained!!!* (16 min video) — https://www.youtube.com/watch?v=viZrOnJclY0
3. IBM Technology — *What is a Vector Database?* (10 min video) — https://www.youtube.com/watch?v=gl1r1XV0SLw
4. OpenAI Cookbook — *Embedding Wikipedia articles for search* (pattern-read; walked through interactively with mentor 2026-09-07: collect → chunk → embed → store → search-on-top) — https://developers.openai.com/cookbook/examples/embedding_wikipedia_articles_for_search
   - **Stack note (probe-verified 2026-09-07):** Ollama Cloud has NO embeddings endpoint (`/v1/embeddings` → 404 route-not-found; chat routes work). Embeddings run on **local Ollama** (`http://localhost:11434/v1`) with `nomic-embed-text` (768 dims, verified by probe). Chat stays on Ollama Cloud. Two clients, one SDK. Recorded for future stack decisions in Weeks 5+.
5. ~~OpenAI Cookbook — *Vector Databases overview*~~ — **REMOVED by OpenAI (cookbook site migration, verified dead 2026-09-06)**. Substitute, deferred to Week 5 where it's more useful anyway: Pinecone — *What is a Vector Database?* (https://www.pinecone.io/learn/vector-database/) + pgvector README (https://github.com/pgvector/pgvector) — the conceptual landscape + the Postgres trade-offs, read together as the "why pgvector" decision basis.

*(Optional deep dive: 3Blue1Brown — Transformers, the tech behind LLMs, "Word embeddings" chapter — https://www.youtube.com/watch?v=wjZofJX0v4M. Replaces the deleted James Briggs items in the Master Resources List too.)*

**Deliverables:**
- `llm-practice/semantic_search.py` — embed a folder of your own notes (the `python-practice/*.md` files work well) and run in-memory cosine-similarity search. No DB yet. Commit the script and one demo run's output.

**Success test:** Explain to a colleague why embedding a query and a document with the same model makes them comparable in vector space. What breaks if you mix models?

**Optional deep dive:** Simon Willison — *Embeddings: what they are and why they matter* — https://simonwillison.net/2023/Oct/23/embeddings/

---

## Phase 2 — RAG, Evals, and Project 1 (Weeks 5–7, 8–10 hrs/week)

### Week 5 — Vector DB with pgvector + RAG basics

**Why pgvector (not Pinecone):** you already know Postgres cold from Walmart. Demonstrating AI engineering on scaled Postgres is a *stronger* story than introducing a new vendor DB. Tier-1 interviews specifically probe "why HNSW vs IVFFlat" — pgvector forces you to learn this.

**Materials:** *(Revised 2026-09-06 — OpenAI Cookbook's pgvector notebook was deleted in the cookbook site migration; substituted with verified equivalents.)*
1. Supabase — *pgvector guide* (90 min, run the embed→store→index→query flow locally with your own Postgres, not Supabase's cloud — same SQL, no lock-in) — https://supabase.com/docs/guides/database/extensions/pgvector — *(covers vector columns, HNSW/IVFFlat indexing, querying in plain SQL; the "Going to production" pages address scaling trade-offs vs dedicated vector DBs)*
   - OpenAI-hosted version of the same flow (live): https://developers.openai.com/cookbook/examples/vector_databases/supabase/semantic-search
2. pgvector README (30 min, focus on the indexing section — HNSW vs IVFFlat) — https://github.com/pgvector/pgvector
3. AWS Prescriptive Guidance — *Vector search in RAG with pgvector* (30 min skim) — https://docs.aws.amazon.com/prescriptive-guidance/latest/retrieval-augmented-generation-options/vector-search.html
4. James Briggs — *Intro to Retrieval Augmented Generation* (30 min video) — https://www.youtube.com/watch?v=u47GtXwePms
5. Anthropic Cookbook — *Chunking with summary index* (60 min) — https://github.com/anthropics/anthropic-cookbook/blob/main/capabilities/retrieval_augmented_generation/chunking_with_summary_index.ipynb

**Deliverables:**
- Small RAG ingestion + query script over a corpus of your choice (your own notes, public docs, or a synthetic corpus you author). Postgres + pgvector in Docker.
- Commit with a README noting: chunking strategy, embedding model, top-k choice, and one example query + retrieved chunks.

**Success test:** Explain why pgvector's HNSW index trades recall for speed. When would you pick IVFFlat instead?

---

### Week 6 — Evals (the #1 gap for backend engineers, per the field guide)

This is the single most important new skill in the entire plan. Do not skip or de-prioritize this week.

**Materials:**
1. Anthropic docs — *Define success* (30 min) — https://platform.claude.com/docs/en/test-and-evaluate/define-success
2. Anthropic docs — *Develop test cases* (45 min) — https://platform.claude.com/docs/en/test-and-evaluate/develop-tests
3. Anthropic docs — *Using the Evaluation Tool* (45 min) — https://platform.claude.com/docs/en/test-and-evaluate/eval-tool
4. Anthropic blog — *Demystifying evals for AI agents* (30 min) — https://claude.com/blog/demystifying-evals-for-ai-agents
5. Anthropic Cookbook — *Building a skills evaluation framework* (60 min, run the notebook) — https://github.com/anthropics/anthropic-cookbook/blob/main/misc/building_skills_evaluation_framework.ipynb
6. DeepLearning.AI short course — *Evaluating AI Agents* (free, ~90 min) — https://www.deeplearning.ai/short-courses/evaluating-ai-agents/

**Deliverables:**
- `llm-practice/evals/` containing:
  - Golden dataset: 15–20 input/output pairs for a small extraction task (e.g., extract {action, owner, due_date} from a meeting notes snippet)
  - LLM-as-judge Python script: Claude (or GPT-4) grades outputs from a cheaper model
  - README: what you measured, why, and what you changed in your prompt based on the eval results
- This README is the single most-quoted-from document in your interviews. Write it carefully.

**Success test:** What's the difference between a grader-based eval, a pairwise-comparison eval, and a trajectory eval? When do you pick each?

**Optional deep dive:** OpenAI — *Evals best practices* — https://platform.openai.com/docs/guides/evals-best-practices

---

### Week 7 — Project 1: Agent Observability Dashboard (heavier week, budget 12–14 hrs realistically)

**Budget honesty check:** the deliverable list below (tracing decorator + Postgres + Grafana dashboard + demo video + README) is a 15+ hour week for most people, even with your infra background. 9–10 hrs was optimistic. Plan for it to spill into a second weekend session, and treat the demo video as a stretch goal (see below) — ship the working dashboard first, add the video before you actually start applying (Week 8), not before this week ends.

**The project:** An end-to-end observability pipeline for agent runs. Wrap an LLM call, capture the trace (prompt, tool calls, latency, tokens, cost), emit it to Postgres, visualize in Grafana.

**Why this project exists:** your SRE background is your moat. Almost nobody coming into AI engineering from DS/research can talk credibly about traces, spans, RED metrics, cost-per-request, error budgets. You can. This project turns that experience into evidence.

**Materials:**
1. Anthropic Cookbook — *Observability and tracing* notebooks (60 min, run both) — https://github.com/anthropics/anthropic-cookbook/tree/main/misc/observability_and_tracing
2. Langfuse — *Observability quickstart (Python)* (45 min, run the `@observe()` decorator example) — https://langfuse.com/docs/observability/get-started
3. Langfuse — *Tracing conceptual overview* (skim) — https://langfuse.com/docs/observability/overview
4. OpenTelemetry Python — *Getting started* (45 min) — https://opentelemetry.io/docs/languages/python/getting-started/
5. OpenTelemetry — *Traces concept* (30 min) — https://opentelemetry.io/docs/concepts/signals/traces/

**Architecture:**
- `agent_trace.py` — a Python decorator / context manager that wraps an agent run and records: prompt, response, tool calls (name, args, duration, status), latency by step, total tokens, estimated cost. Emits structured JSON to Postgres.
- Postgres in Docker (plain tables — pgvector not needed for this project)
- **Grafana dashboard over Postgres** (your Walmart SRE stack — huge narrative win):
  - Time-series: runs/hour, success vs failure rate, p50/p95 latency
  - Breakdown: tool-call counts, error rate by tool, cost per day
  - Single-run drill-down: timeline of a run's spans
- README with: problem statement, architecture diagram (mermaid), cost/latency reasoning, screenshots of the dashboard

**Deliverables:**
- New repo `agent-observability/` on GitHub with the above. This is the hard requirement to call the week "shipped."
- *(Stretch, not blocking)* A 60-second Loom or QuickTime demo video embedded in the README — add this during Week 8 if it doesn't fit this week.

**Success test:** Show one bad agent run. Click through to the failing tool call. Tell me what it cost.

**If time allows this week (30–45 min, not required):** do a *light* pass on your resume — just enough to lead with the platform+reliability narrative and list Project 1 as a shipped GitHub link. This is not the full rewrite (that's Week 12) — it's just enough to start low-volume applications in Week 8 without waiting until Week 13. If it doesn't fit, push it into the start of Week 8; don't let it eat into Project 1 shipping.

---

## Phase 3 — Agents + Project 2 (Weeks 8–11, 8 hrs/week)

**Note on Weeks 10–11:** these are protected build time for Project 2. No interview-prep tasks are scheduled here on purpose — the original draft of this plan crammed resume work into these same two weeks and one of the two would have suffered. Resist the urge to start "just a quick resume pass" here; it has a dedicated week later (Week 12).

### Week 8 — LangGraph + MCP foundations

**Materials:**
1. LangChain Academy — *Introduction to LangGraph* (free course, ~3 hrs; the canonical resource) — https://academy.langchain.com/courses/intro-to-langgraph
2. MCP Python SDK quickstart — *Build a server* (60 min, run it — expose your first tool) — https://modelcontextprotocol.io/quickstart/server
3. MCP Python SDK README (30 min skim examples) — https://github.com/modelcontextprotocol/python-sdk
4. Anthropic blog — *Code execution with MCP* (30 min skim — explains *why* MCP matters) — https://claude.com/blog/code-execution-with-mcp

**Deliverables:**
- `llm-practice/langgraph_tutorial/` folder with tutorial work committed as you go
- `llm-practice/mcp_server_demo.py` — minimal MCP server exposing one tool (e.g., calculator) tested with Claude Desktop

**Success test:** Explain LangGraph's state / nodes / edges model. How does it differ from a chain? When do you want a graph?

**Optional deep dive:** DeepLearning.AI — *AI Agents in LangGraph* — https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/

---

### Week 9 — Project 2 MCP server

**Materials:**
1. MCP quickstart server — revisit in depth — https://modelcontextprotocol.io/quickstart/server
2. MCP full spec (skim, only the conceptual sections you need) — https://modelcontextprotocol.io/specification/latest
3. Awesome MCP servers (15 min skim to see the landscape) — https://github.com/punkpeye/awesome-mcp-servers

**Deliverables:** new repo `delivery-ops-mcp/` — a real MCP server exposing 2–3 tools:
- `lookup_delivery_status(tracking_id) -> DeliveryStatus` — backed by synthetic Postgres data you generate
- `check_weather(zip: str, date: date) -> WeatherReport` — wraps OpenWeatherMap free tier OR a deterministic stub
- `get_delivery_policy(query: str) -> list[PolicyChunk]` — RAG over a small policy-docs corpus you author (this is where pgvector from Week 5 comes back into play)

Test it with Claude Desktop.

**Success test:** Connect your server to Claude Desktop, ask it to triage a synthetic late delivery — does Claude call your tools in the right order?

---

### Weeks 10–11 — Project 2: Delivery-Ops Triage Agent

**The project:** A LangGraph agent that triages last-mile delivery exceptions end-to-end. Calls your MCP server's tools, handles multi-step workflows, includes guardrails and evals, and emits traces through Project 1's pipeline.

**Materials:**
1. Anthropic — *Building Effective Agents* — re-read Part 2 (orchestrator + evaluator) — https://www.anthropic.com/engineering/building-effective-agents
2. LangGraph — *Why LangGraph?* (conceptual overview) — https://langchain-ai.github.io/langgraph/concepts/why-langgraph/
3. Anthropic Cookbook — *Agents patterns* + *Multi-agent orchestration* (90 min) — https://github.com/anthropics/anthropic-cookbook/tree/main/patterns/agents
4. Anthropic blog — *How we built our multi-agent research system* (30 min skim) — https://www.anthropic.com/engineering/multi-agent-research-system
5. Anthropic blog — *Building agents with the Claude Agent SDK* (60 min) — https://claude.com/blog/building-agents-with-the-claude-agent-sdk

**Architecture:**
- LangGraph graph shape:
  ```
  triage_node ─→ tool_node (calls MCP server) ─→ reasoning_node ─→ action_node
        ↑                                                        │
        └────────── (conditional edge, loop back if more info needed) ──┘
  ```
- ReAct-style loop with `max_iterations=5` guard
- **Guardrails**: tool-timeout retry (exponential backoff, max 2 retries), hallucination validator pass (LLM-as-judge from Week 6) before final action
- Every run emitted through Project 1's `agent_trace.py` → Grafana dashboard lights up

**Deliverables:**
- New repo `delivery-ops-agent/` with the above
- README containing: problem, architecture diagram (mermaid), cost-per-triage analysis, design-decision log ("why LangGraph not raw SDK", "why MCP for tools"), evals methodology and results
- 2-minute demo video (Loom or QuickTime) linked in README
- Both Project 1 + Project 2 READMEs cross-link to each other — explicitly frame them as one composable system

**Success test:** Walk me through one full triage run. Where did it cost the most? Where would you add guardrails if this were production at Walmart scale?

**Optional deep dive:** Anthropic Academy — *AI Fluency: Framework & Foundations* — https://anthropic.skilljar.com/ai-fluency-framework-foundations

---

## Phase 4 — Interview Sprint (Weeks 8–16, ramping 2→6 hrs/week, running around the protected Project 2 build in Weeks 10–11)

### Week 8 — Begin light applications (1–2/week, calibration mode)

This starts as soon as Project 1 is live and the light resume pass from end-of-Week-7 exists. Purpose: get real feedback on your resume and narrative early, warm up interview muscle, and avoid a cold start in Week 13. These are *not* your top-target applications yet.

- Apply to 1–2 **Tier 3** postings this week (large-tech AI-platform teams) — lower stakes, good for calibrating whether your resume/narrative lands
- Note any recruiter/ATS feedback (auto-rejects, callback rate) — this is signal for the Week 12 resume rewrite
- Keep this light — the real budget for this week is still Project 2 prep (Week 8 material from Phase 3)

### Week 9 — Internal Walmart recon (runs alongside Project 2 build)

- Identify agentic AI / AI platform teams internally (Confluence, org chart, your network)
- 2–3 informational chats. No hard ask — gather intel, warm relationships
- If Walmart's agentic AI direction looks strong, this becomes a real option; if not, you've lost a couple hours
- Low-effort by design — Weeks 9's real budget is LangGraph/MCP build work

*(Weeks 10–11: no Phase 4 tasks — see the protected-build note in Phase 3. Continue the 1–2/week Tier 3 applications from Week 8 on autopilot if you have a template ready, but don't add new prep work.)*

### Week 12 — Full resume rewrite + behavioral story bank (dedicated week, no project competing)

Both projects are shipped by now — this is the first week where interview prep gets full, undivided attention.

**Materials:**
- Field guide — *Skills that get you hired* — https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/interview/03-get-hired.md
- Field guide — *Interview process overview* — https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/interview/01-interview-process.md
- STAR method overview (30 min) — https://www.themuse.com/advice/star-interview-method
- Field guide — *Project deep dive* — https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/interview/questions/03-project-deep-dive.md

**Deliverables:**
- New resume: lead with "Staff backend engineer — platform + reliability — extending to agentic AI systems." **Do NOT** lead with "learning AI" or "aspiring AI engineer." Fold in whatever you learned from Week 8's calibration applications.
- 2–3 trusted reviewers have given feedback on the resume
- `interview-prep/stories.md` — 6–8 STAR-format stories drawn from real work (last-mile delivery incidents, dev-tooling adoption wins, SRE production saves, Project 1/2 build decisions). Cover: conflict, failure, leading under ambiguity, technical deep-dive, mentoring/influence without authority. These get reused across every behavioral round — write them once, carefully.

### Week 13 — Technical question bank + AI system design prep + ramp applications to full volume

**Materials:**
- Field guide — *Theory questions* — https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/interview/questions/01-theory.md
- Field guide — *AI system design* (this is where you differentiate at Staff level) — https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/interview/questions/04-ai-system-design.md
- Field guide — *Company-by-company interview data* — read the entry for each company **before** you apply: https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/interview/data
- Field guide — *Job market trends* — vocabulary alignment with current postings: https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/job-market/trends.md

**Deliverables:**
- `interview-prep/answers.md` — your own-word outlines for the ~10 most-likely theory/system-design questions. Update after every real interview.
- Applications ramp to **5–8/week**, Tier 1 first, then Tier 2, then Tier 3. Priority order for each week's batch: Tier 1 first.

**Cover letter / application note template:**
> Staff backend / SRE engineer (7y at Walmart Global Tech) transitioning to agentic AI. Two shipped Python projects on my GitHub: an agent-observability dashboard (Grafana/Postgres/OTel-style traces) and a LangGraph delivery-triage agent with MCP tools + evals, wired into the same observability pipeline. Both READMEs document cost/latency and failure-mode reasoning. Recent work: [link to most relevant project].

### Week 14 — Practice + take-home pipeline

**Materials:**
- Field guide — *Home assignments* — https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/interview/questions/06-home-assignments.md
- Field guide — *Coding round* — https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/interview/questions/02-coding.md
- Pramp or interviewing.io — book 1–2 mock AI system-design sessions

**Deliverables:**
- 1 take-home style repo scaffolded in advance (so when a real one comes, you're not scaffolding from zero)
- 2 mock system-design sessions completed
- 1 mock behavioral round (use the Week 12 story bank) — a friend, mentor, or Pramp works

### Weeks 15–16 — Pipeline builds; iterate on weak spots

- Interview loops continue. After each one: 15-min self-debrief, update `interview-prep/answers.md` and `interview-prep/stories.md` with what surprised you
- If external offers are close: engage internal Walmart track with real negotiating leverage
- This is also where you decide whether to extend the plan by 2 weeks if the pipeline needs more time — given Tier-1 hiring loops often run 4–8 weeks themselves, treat Week 16 as "pipeline fully in motion," not "offers in hand." Offers landing in early Q1 2027 is a realistic, not-behind-schedule outcome.

---

## Cross-Cutting Habits (every week, all 16 weeks)

1. **Sunday 15-min check-in** — what got done, what's blocking, ONE thing for next week. Consistency > intensity. A 16-week plan that takes 20 weeks because life happened is still a win.
2. **Commit as you learn.** `llm-practice/`, Project 1, Project 2 — green squares matter on your GitHub profile.
3. **README quality bar** — every repo has: problem, architecture diagram (mermaid), cost/latency reasoning, "why I chose X" section, how to run, screenshots or demo video. This is what separates Staff from Senior in interviews.
4. **Cost/latency reasoning habit** — every project README has an explicit "why" for: model choice, retrieval approach, vector DB choice, judge model, observability stack. Interviewers at Anthropic/OpenAI probe these.
5. **The narrative** — every artifact should be evidence for: *"platforms + reliability → agentic AI."*

---

## Master Resources List (organized by topic)

### Field guide (backbone reference)
- Repo root — https://github.com/alexeygrigorev/ai-engineering-field-guide
- Role analysis — https://github.com/alexeygrigorev/ai-engineering-field-guide/tree/main/role
- Interview prep — https://github.com/alexeygrigorev/ai-engineering-field-guide/tree/main/interview
- Backend-engineer learning path — https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/learning-paths/from-backend-engineer.md

### Python wrap-up
- Corey Schafer async playlist — https://www.youtube.com/playlist?list=PL-osiE80TeTsW6VCPUiN9131_VKHFt2D4
- Real Python async walkthrough — https://realpython.com/async-io-python/
- FastAPI First Steps — https://fastapi.tiangolo.com/tutorial/first-steps/

### LLM APIs & structured outputs
- OpenAI structured outputs — https://platform.openai.com/docs/guides/structured-outputs
- OpenAI function calling — https://platform.openai.com/docs/guides/function-calling
- Anthropic tool use — https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview
- Anthropic Cookbook (Pydantic tool use) — https://github.com/anthropics/anthropic-cookbook/blob/main/tool_use/tool_use_with_pydantic.ipynb

### Prompt engineering
- Anthropic prompt engineering docs — https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview
- Anthropic interactive tutorial — https://github.com/anthropics/prompt-eng-interactive-tutorial
- Anthropic *Building Effective Agents* — https://www.anthropic.com/engineering/building-effective-agents
- (Optional) Lilian Weng — https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/

### Embeddings & vector DBs
- Pinecone — *What are Vector Embeddings?* — https://www.pinecone.io/learn/vector-embeddings/
- StatQuest — *Word Embedding and Word2Vec, Clearly Explained!!!* — https://www.youtube.com/watch?v=viZrOnJclY0
- IBM Technology — *What is a Vector Database?* — https://www.youtube.com/watch?v=gl1r1XV0SLw
- OpenAI Cookbook — Wikipedia embeddings search — https://developers.openai.com/cookbook/examples/embedding_wikipedia_articles_for_search
- Pinecone — *What is a Vector Database?* — https://www.pinecone.io/learn/vector-database/
- Supabase pgvector guide — https://supabase.com/docs/guides/database/extensions/pgvector
- pgvector — https://github.com/pgvector/pgvector

### Evals
- Anthropic *Define success* — https://platform.claude.com/docs/en/test-and-evaluate/define-success
- Anthropic *Develop test cases* — https://platform.claude.com/docs/en/test-and-evaluate/develop-tests
- Anthropic *Demystifying evals* blog — https://claude.com/blog/demystifying-evals-for-ai-agents
- Anthropic Cookbook — *Skills eval framework* — https://github.com/anthropics/anthropic-cookbook/blob/main/misc/building_skills_evaluation_framework.ipynb
- DeepLearning.AI — *Evaluating AI Agents* — https://www.deeplearning.ai/short-courses/evaluating-ai-agents/

### Observability & tracing
- Anthropic Cookbook — *Observability & tracing* — https://github.com/anthropics/anthropic-cookbook/tree/main/misc/observability_and_tracing
- Langfuse quickstart — https://langfuse.com/docs/observability/get-started
- OpenTelemetry Python getting started — https://opentelemetry.io/docs/languages/python/getting-started/

### LangGraph & agents
- LangChain Academy — https://academy.langchain.com/courses/intro-to-langgraph
- LangGraph *Why LangGraph* — https://langchain-ai.github.io/langgraph/concepts/why-langgraph/
- Anthropic Cookbook — *Agents patterns* — https://github.com/anthropics/anthropic-cookbook/tree/main/patterns/agents
- Anthropic — *Multi-agent research system* — https://www.anthropic.com/engineering/multi-agent-research-system
- Anthropic — *Claude Agent SDK* — https://claude.com/blog/building-agents-with-the-claude-agent-sdk

### MCP
- MCP Python SDK — https://github.com/modelcontextprotocol/python-sdk
- MCP *Build a server* quickstart — https://modelcontextprotocol.io/quickstart/server
- Anthropic — *Code execution with MCP* — https://claude.com/blog/code-execution-with-mcp

### Interview prep
- Field guide — *Get hired* — https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/interview/03-get-hired.md
- Field guide — *Theory questions* — https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/interview/questions/01-theory.md
- Field guide — *AI system design* — https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/interview/questions/04-ai-system-design.md
- Field guide — *Project deep dive* — https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/interview/questions/03-project-deep-dive.md
- Field guide — *Home assignments* — https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/interview/questions/06-home-assignments.md
- Field guide — *Company-by-company data* — https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/interview/data

### Behavioral prep
- STAR method overview — https://www.themuse.com/advice/star-interview-method
- Draw stories from: last-mile delivery incidents, dev-tooling adoption wins, SRE production saves, Project 1/2 design decisions

---

## Progress Tracker

Update after each week. (Mark `[x]` when complete.)

### Phase 0 — Python wrap-up
- [x] Week 1 — Gym re-green, async/await, lint setup (FastAPI deferred to Week 7 if needed) — **COMPLETE 2026-08-25**
- [x] Gym refresh — reviewed Python fundamentals 2026-08-24
- [x] ex08 async/await module added to gym and completed (15/15 green) — covers coroutines, gather/create_task, timeouts/cancellation, async generators, async context managers

**PHASE 0 COMPLETE.** Next: Week 2 — OpenAI + Anthropic SDKs, structured outputs, function calling.

### Phase 1 — LLM Foundations
- [x] Week 2 — OpenAI + Anthropic SDKs, structured outputs, function calling — **COMPLETE 2026-08-29**
- [x] Week 3 — Prompt engineering + versioning — **COMPLETE 2026-09-05** (promptfoo eval: v1 0/14 vs v2 6/14; adversarial lab; schema-migrations doc)
- [ ] Week 4 — Embeddings + semantic search

### Phase 2 — RAG + Evals + Project 1
- [ ] Week 5 — pgvector + RAG basics
- [ ] Week 6 — Evals (golden dataset, LLM-as-judge)
- [ ] Week 7 — **Project 1: Agent Observability Dashboard shipped**

### Phase 3 — Agents + Project 2
- [ ] Week 8 — LangGraph + MCP foundations
- [ ] Week 9 — Project 2 MCP server shipped
- [ ] Week 10 — Project 2 core agent loop working
- [ ] Week 11 — **Project 2: Delivery-Ops Triage Agent shipped, wired into Project 1**

### Phase 4 — Interview sprint (decoupled from project build weeks)
- [ ] Week 7 (tail end) — Light resume/narrative pass, Project 1 linked
- [ ] Week 8 — Light applications begin (1–2/week, Tier 3, calibration mode)
- [ ] Week 9 — Internal Walmart recon (2–3 chats)
- [ ] Weeks 10–11 — *(protected build — no Phase 4 tasks, autopilot Tier 3 applications only)*
- [ ] Week 12 — Full resume rewrite + behavioral story bank (`stories.md`)
- [ ] Week 13 — Technical question bank + AI system design prep; ramp to 5–8 applications/week, Tier 1 first
- [ ] Week 14 — Mock system-design + take-home scaffold + mock behavioral round
- [ ] Week 15 — Pipeline in motion
- [ ] Week 16 — Iterating on interviews; expect offers to land into early Q1 2027, not necessarily by Week 16

---

*Plan lives in git. Edit as life happens. Progress > perfection.*
