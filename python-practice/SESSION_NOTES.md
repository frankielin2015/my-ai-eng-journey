# Session Notes / Handoff

> A running log so we can pick up the conversation right where we left off.
> Reed (your Python instructor puppy) keeps this updated at handoff time.

---

## How to resume next session

Tell Reed: **"Read SESSION_NOTES.md and let's continue."** That rehydrates
everything below. Then jump back into whatever's marked IN PROGRESS.

Quick commands:
```bash
uv run python progress.py                              # scoreboard
uv run pytest tests/test_ex03_data_structures.py -v    # work one module
uv run pytest                                           # everything
```

---

## Progress (as of last session)

| # | Module | Status |
|---|--------|--------|
| 01 | ex01_syntax_basics | DONE (10/10 green) |
| 02 | ex02_builtins | DONE (11/11 green) |
| 03 | ex03_data_structures | DONE (all green) |
| 04 | ex04_comprehensions | DONE (all green) |
| 05 | ex05_oop_basics | DONE (8/8) -- but `withdraw` has a lurking bug (see below) |
| 06 | ex06_oop_advanced | DONE (9/9 green) |
| 07 | ex07_generators_errors | DONE (all green) |
| 08 | ex08_async_await | DONE (15/15 green) |

**STATUS: ENTIRE GYM COMPLETE -- 82/82 tests green, 8/8 modules.**
Student finished ex01-ex08. Async/await covered in ex08 (coroutines, gather,
create_task, timeouts/cancellation, async generators, async context managers).
**Phase 0 of the AI transition plan is now CLOSED.** Next: Week 2 of
`../ai-engineer-transition-plan.md` — OpenAI + Anthropic SDKs, structured
outputs, function calling.

---

## Open review note in ex05 (student chose to leave it -- gym, not prod)

- `BankAccount.withdraw` never rejects `amount <= 0`. `withdraw(-50)` on a
  $10 balance yields $60 (subtracting a negative = free money). Tests pass
  because none throw a negative -> same coverage-gap lesson as `all_positive`.
  Spec-correct fix: `if amount <= 0 or amount > self.balance: raise
  ValueError("Insufficient funds")`. Student understood the concept
  (green tests != correct); left it since it's a learning gym.

## Open review notes to double-check in ex02

These passed the tests but have lurking issues we discussed (student may or
may not have patched them yet -- verify on resume):

- `all_positive` had a REAL bug: `all(numbers)` checks truthiness, not sign.
  `all([1, -2, 3])` wrongly returns True. Fix: `all(n > 0 for n in numbers)`.
  Tests passed only because they never included a negative -> coverage gap.
- `only_even` still used `filter + lambda`; linter prefers a comprehension:
  `[x for x in numbers if x % 2 == 0]`.
- `index_each` was a pass-through repack of `enumerate`; cleaner as
  `list(enumerate(items))`.

---

## Concepts covered so far (student's mental model)

Student is a Walmart STAFF ENGINEER: strong in Node/TS, some Java, some
React, mostly backend. Learning Python for AI work. Did Codecademy's
"Python for Programmers" (data structures + OOP). Wants hands-on practice
to internalize syntax, built-ins, data structures, OOP idioms. Teach with
TS/Java analogies; he learns fast and asks great "why" questions.

Topics we went deep on:
- **Type hints** are optional & NOT enforced at runtime (like TS types being
  erased). `mypy`/`pyright` check them as a separate step. `int | None` =
  union. `list[int]`/`dict[str,int]` = generics.
- **`*args` / `**kwargs`** = JS rest params. `*` collects (in def) and
  spreads (in calls); `**` is the dict/keyword version.
- **Truthiness**: only zero/empty are falsy. ALL nonzero numbers (incl.
  negatives) are truthy. Bit him twice (`any(numbers)`, `all(numbers)`).
  Rule: with any()/all(), spell out the condition via a generator expr.
- **Comprehensions** (the big one): `[expr for x in it if cond]`. Four kinds
  -- list `[]`, set `{}`, dict `{k:v}`, generator `()`. Fuses map+filter into
  one pass (vs TS's `.filter().map()` chaining). Linter flags `map`/`filter`
  + `lambda` -> use a comprehension. But DON'T force it for pass-throughs
  (e.g. `list(zip(...))` and `list(enumerate(...))` are already ideal).
- **Sets vs dicts**: `{}` is an empty DICT, not a set -- must use `set()`.
  Set has `.add()`, dict has `.get()`. He mixed these up in dedupe.
- **Dict iteration defaults to KEYS**: `list(d)`, `for k in d`, `x in d` all
  hit keys. Use `.values()`, `.items()` explicitly. `.items()` = JS
  `Object.entries`. `dict.fromkeys(seq)` -> ordered unique keys w/ None values;
  `list(...)` of it = one-line ordered dedupe.
- **ex06 OOP went DEEP** (student asked great questions, now solid on):
  - **Decorators**: `@deco` = `foo = deco(foo)`. Not passive like Java
    annotations -- they transform the thing below.
  - **Dunders**: `__add__`/`__eq__`/`__repr__`/`__abs__` = operator/builtin
    hooks. `a + b` -> `a.__add__(b)`. `&`/`&&` trap: use `and` (logical) not
    `&` (bitwise). `!` doesn't exist alone -> `not`; but `!=` is fine.
  - **@property**: getter/setter as field syntax. Traced internals hard --
    property object has `fget`/`fset`/`fdel` slots (None until filled).
    `@x.setter` returns a NEW property (immutable), rebinds the name. Needs a
    separate `_celsius` storage or infinite recursion. `_celsius` born only
    on first setter assignment. Getter+setter MUST share the name.
  - **@dataclass**: auto-gens `__init__`/`__repr__`/`__eq__` from annotated
    fields. The ONE place type annotations are load-bearing at runtime.
    Stepping stone to Pydantic BaseModel (relevant to his AI goal).
  - **@staticmethod** (no self/cls, = Java static) vs **@classmethod**
    (`cls` = the class; killer use = alt constructors like `dict.fromkeys`).
- **type hints = TS types**: built into `.py` syntax (free), IGNORED at
  runtime, checked by SEPARATE optional tool (`mypy`/`pyright`) like `tsc`.
  Unlike TS, `.py` always runs w/o a compile step. Repo has NO checker
  installed yet (offered ruff+pyright, he deferred). Industry standard =
  type your boundaries + checker in CI. FastAPI/Pydantic are types-first.

---

## Environment notes

- Python 3.13.5, `uv`-managed venv (`.venv/`), pytest.
- `pyproject.toml` pins the Walmart pip index so `uv run` works on-network.
- Git initialized; commit often.
- Emojis are stripped from file writes in this project (hook enforced).

---

## Side conversation (career -- worth remembering)

Student opened up about post-AI career anxiety: pre-AI work (CRUD, APIs,
tests, microservices, PRD meetings) had a satisfying struggle->resolution
loop; AI compressed that, leaving a hollow feeling + fear of "being behind"
while others build skills/MCPs. Reed's take: the fear is a lagging indicator
(conscientious-person tax), not reality -- he's ahead. The bottleneck moved
from *production* to *orchestration + verification + taste*. His sense that a
lot of new busywork is "meaningless" IS taste, not cynicism. MCPs/skills are
just plumbing, not a higher plane -- chasing them = new CRUD treadmill. Real
shift: identity from "I build the solution" -> "I decide what's worth solving
and vouch for the result." Learning Python IS the right call: it's the
steering wheel for trusting/debugging AI output. Open thread: what kind of
problem still gives him the "click"? That's the compass for where to point
his newfound leverage. Be warm and real if this comes up again.
