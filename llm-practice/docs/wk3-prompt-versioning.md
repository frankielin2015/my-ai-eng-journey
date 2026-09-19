# Week 3 — Prompt Versioning: Schema Migrations, Different Artifact

_Success test: explain prompt versioning as analogous to schema migrations —
same discipline, different artifact. This doc is that explanation, with the
war stories to back it._

## The analogy

A database schema is a contract between the DB and every client that touches
it. Changing it carelessly breaks consumers you can't see. So we developed a
discipline: versioned migrations, recorded changes, never edit what's released,
regression-test before shipping.

An LLM prompt is the same kind of contract. `sentiment_v2.md` defines an
interface: `{{user_text}}` placeholder in, `<thinking>...</thinking>` fence +
JSON object out, four keys, a four-value enum. Downstream "clients" are real
code — `lab_sentiment.py`'s `render()` writes into the contract,
`classify()`'s `split("</thinking>")[-1]` parses out of it, Pydantic enforces
the schema at the boundary. Change the prompt carelessly and you break those
consumers in exactly the way an API change breaks clients — except nothing
throws at deploy time. The breakage is silent: extraction grabs the wrong
text, validation fails downstream, and the dashboard shows errors instead of
a build going red.

So the discipline ports:

| Schema migrations | Prompt versioning |
|---|---|
| versioned migration files | `sentiment_v1.md`, `sentiment_v2.md` |
| migration changelog | `prompts/CHANGELOG.md` |
| never edit a released version | v1 stays frozen as the control |
| regression suite before shipping | promptfoo eval (v1 vs v2 delta) |
| client contract (typed queries) | downstream parser + Pydantic schema |

## Three war stories

**1. The "mixed" enum gap — a taxonomy bug found by prompt review.**
v1's schema had `positive | negative | neutral`. While writing v2's multishot
examples, the boundary case "Great camera but the battery dies by noon" had
no valid label — the taxonomy was wrong, not the prompt. The fix was a real
migration: widen the enum to `+mixed` in the Pydantic schema
(`ex2_sentiment_extractor.py`), recorded in the CHANGELOG alongside the
prompt change. Lesson: prompt work surfaces schema gaps — the prompt and its
output schema are one contract, and changing either is a migration.

**2. Never edit a released version.**
When the first seeded probe came back ambiguous, the temptation was to tweak
v2's wording in place. Instead: v2 stays as-is, findings recorded, any fix
becomes a v3 with its own CHANGELOG entry and eval run. Same reason you don't
`UPDATE` a released migration — the control condition (v1) and the treatment
(v2) only mean something if neither moves mid-experiment.

**3. The confounded probe — an eval only measures what its probe can
distinguish.**
First seeded-anchoring probe: review mildly positive, seeded `<thinking>`
concludes "positive, 0.99." Both roads led to `positive` — the run couldn't
tell honest judgment from steering. Fixed by making the seed contradict the
review (negative review, positive seed). Only then did the matrix measure
anything. This is test design, not prompt engineering — and it's why Week 6
evals start from "what outcome separates the hypotheses?" before writing
test cases.

## The measured result (promptfoo, 2026-09-05)

7 tests × 2 prompts × 2 models, Ollama Cloud:

- **v1: 0/14. v2: 6/14** (kimi 6/7, gpt-oss 0/7)
- v1's "Respond with ONLY a JSON object" is a request, not a contract — with
  no server-side JSON enforcement (Ollama Cloud, see wk2 quirks), both
  models drifted into free-form reasoning prose. 0% parseable.
- v2's multishot examples (schema-exact output templates) pulled kimi into
  compliance. Structure teaches structure: the model copies the shape it
  sees.
- gpt-oss:20b ignored both prompts' output contracts and emitted its native
  `Thinking:` format — the same prompt is a contract for one model and a
  suggestion for another. Model choice and per-model behavior measurement
  are load-bearing engineering decisions, not footnotes.

## What I'd tell an interviewer

Prompt versioning *is* schema migration discipline applied to a new artifact:
frozen released versions, a changelog that records what/why/measured-effect,
and a regression suite gating changes. The new wrinkles vs. databases:
prompts are trivially easy to change and hard to verify (hence the eval
harness), model compliance with the "schema" is partial (hence client-side
validation as the only portable guarantee — measured, not assumed), and eval
probes must be designed to discriminate (a confounded test measures nothing).