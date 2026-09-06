#  Python Practice Gym

A TDD-style practice course built for an experienced backend engineer
(TS/Java/React) ramping up on Python. Each topic is a **skeleton module**
with functions stubbed out — your job is to fill them in. A matching
**pytest suite** gives you instant green/red feedback.

## The loop

1. Open an exercise file in `exercises/`.
2. Replace each `raise NotImplementedError` (and `TODO`s) with real code.
3. Run that module's tests until they're green.
4. Repeat. Check your overall progress anytime.

## Commands

```bash
# Run ONE module's tests (recommended while working)
uv run pytest tests/test_ex01_syntax_basics.py -v

# Run everything
uv run pytest

# See your scoreboard
uv run python progress.py
```

> All tests start RED (they call unimplemented stubs). That's expected —
> turning them green is the whole game. 

## Curriculum

| # | Module | What you'll practice |
|---|--------|----------------------|
| 01 | `ex01_syntax_basics` | functions, default/`*args`/`**kwargs`, conditionals, loops, ternary, tuple unpacking, walrus |
| 02 | `ex02_builtins` | `sum`/`min`/`max`/`sorted`/`enumerate`/`zip`/`map`/`filter`/`any`/`all`/`round` |
| 03 | `ex03_data_structures` | list/dict/set/tuple ops, counting, grouping, set algebra |
| 04 | `ex04_comprehensions` | list/dict/set/nested comprehensions + string methods & slicing |
| 05 | `ex05_oop_basics` | classes, `__init__`, instance vs class attrs, `__str__` |
| 06 | `ex06_oop_advanced` | inheritance/`super`, dunders, `@property`, `@dataclass`, `@staticmethod`/`@classmethod` |
| 07 | `ex07_generators_errors` | `yield`, generators, `try/except/finally`, custom exceptions, context managers |
| 08 | `ex08_async_await` | coroutines, `async`/`await`, `asyncio.gather`, `asyncio.create_task`, timeouts/cancellation, async generators, async context managers |

## Tips from your instructor 

- **Read the docstrings** — each one tells you exactly what's expected,
  often with example inputs/outputs and a Pythonic hint.
- **Pythonic > clever.** Reach for built-ins and comprehensions before
  hand-rolling loops. The tests don't care *how*, but you're here to
  learn the idioms.
- **`uv run python`** drops you into a REPL with the venv active — great
  for experimenting before committing to an answer.
- Stuck? Ask me (Reed) to explain a concept or review your solution.

Have fun. Make 'em green. 
