"""
Exercise 08 — Async / Await in Python
=====================================

Async is the concurrency model used everywhere in modern Python AI code —
LLM SDKs (OpenAI, Anthropic), LangGraph, MCP servers, FastAPI. It's not
threads: it's a single event loop juggling many coroutines that cooperate
by yielding control at `await` points.

    uv run pytest tests/test_ex08_async_await.py -v

Topics: coroutines (`async def` / `await`), tasks, `asyncio.gather`,
`asyncio.create_task`, timeouts, cancellation, async generators `async for`,
async context managers `async with`.
"""
from __future__ import annotations

import asyncio
from typing import AsyncIterator

import time


# ---------------------------------------------------------------------------
# Part 1 — Coroutines: defining & awaiting
# ---------------------------------------------------------------------------

async def async_identity(value):
    """The simplest coroutine: just return `value`.

    In Java terms: like a method that returns a CompletableFuture, but
    the body doesn't run until something `await`s it.
    """
    # TODO: raise NotImplementedError → return value
    return value

async def async_add(a: int, b: int) -> int:
    """An async function that returns a + b. Point: async functions can
    take args and return values like sync ones — the only difference is the
    `async def` and that callers must `await` them.

    async_add(20, 22) should give 42 (when awaited).
    """
    return a + b


async def call_an_async_function(x: int) -> int:
    """Call asyncio.sleep(0) inside this coroutine (yield control back to
    the event loop), then return x * 2.

    This is the pattern you'll use when your coroutine needs to cooperate
    with other coroutines — asyncio.sleep(0) is the explicit yield point.
    """
    # TODO: await asyncio.sleep(0); return x * 2
    await asyncio.sleep(0)
    return x * 2


# ---------------------------------------------------------------------------
# Part 2 — Concurrency: gather & create_task
# ---------------------------------------------------------------------------

async def fake_io(name: str, delay: float) -> str:
    """Simulates an IO call: sleeps for `delay` seconds, then returns a
    string like "name done".

    Use this in the exercises below — do NOT modify.
    """
    await asyncio.sleep(delay)
    return f"{name} done"


async def run_sequentially() -> list[str]:
    """Run three fake_io() calls SEQUENTIALLY (one after another) and
    return their results in order.

    - fake_io("a", 0.01)
    - fake_io("b", 0.01)
    - fake_io("c", 0.01)

    Expected elapsed: ~0.03s.
    """
    # TODO: result_a = await fake_io("a", 0.01); result_b = await fake_io(...)
    result_a = await fake_io("a", 0.01)
    result_b = await fake_io("b", 0.01)
    result_c = await fake_io("c", 0.01)
    return [result_a, result_b, result_c]


async def run_concurrently() -> list[str]:
    """Run the SAME three fake_io() calls CONCURRENTLY using
    asyncio.gather() and return their results in order.

    Expected elapsed: ~0.01s (the longest of the three).

    This is the core pattern for calling many LLM APIs in parallel.
    """
    # TODO: results = await asyncio.gather(fake_io("a", 0.01), fake_io("b", 0.01), fake_io("c", 0.01))
    results = await asyncio.gather(
        fake_io("a", 0.01),
        fake_io("b", 0.01),
        fake_io("c", 0.01)
    )
    return results


async def run_with_create_task() -> list[str]:
    """Run the three fake_io() calls using asyncio.create_task() — a more
    explicit API than gather. Create three tasks, then await each one and
    collect results in the same order.

    create_task schedules the coroutine to run "soon"; the await then waits
    for the result. Useful when you want to do work between scheduling and
    waiting.
    """
    # TODO: t_a = asyncio.create_task(fake_io("a", 0.01)); ...; return [await t_a, await t_b, await t_c]
    task_a = asyncio.create_task(fake_io("a", 0.01))
    task_b = asyncio.create_task(fake_io("b", 0.01))
    task_c = asyncio.create_task(fake_io("c", 0.01))
    return [await task_a, await task_b, await task_c]

# ---------------------------------------------------------------------------
# Part 3 — Timeouts, cancellation, error handling
# ---------------------------------------------------------------------------

async def slow_call() -> str:
    """Simulates a hung LLM call: sleeps for 10 seconds, returns "done".
    """
    await asyncio.sleep(10)
    return "done"


async def cancel_slow_call() -> str:
    """Run slow_call(), but cancel it after 0.01 seconds using
    asyncio.wait_for(). When it times out, return "cancelled".

    Catches asyncio.TimeoutError. This is the pattern for "give up on a
    hanging LLM call."
    """
    
    # TODO: try: return await asyncio.wait_for(slow_call(), timeout=0.01)
    #       except asyncio.TimeoutError: return "cancelled"
    try:
        return await asyncio.wait_for(slow_call(), timeout=0.01)
    except asyncio.TimeoutError:
        return "cancelled"


async def gather_with_errors() -> list[str | BaseException]:
    """Run three coroutines concurrently with asyncio.gather():
    - fake_io("ok1", 0.01)
    - a coroutine that raises ValueError("boom")
    - fake_io("ok2", 0.01)

    Use `return_exceptions=True` so failures come back as values instead of
    crashing the whole gather. Return the results — two strings and the
    ValueError instance.
    """
    # TODO: async def failing(): raise ValueError("boom")
    #       return await asyncio.gather(fake_io(...), failing(), fake_io(...), return_exceptions=True)
    async def failing():
        raise ValueError("boom")
    return await asyncio.gather(fake_io("ok1", 0.01), failing(), fake_io("ok2", 0.01), return_exceptions=True)


# ---------------------------------------------------------------------------
# Part 4 — Async generators & async context managers
# ---------------------------------------------------------------------------

async def async_countdown(n: int) -> AsyncIterator[int]:
    """An ASYNC GENERATOR that yields n, n-1, ..., 1, sleeping 0.001s
    between yields.

    Consumed as:
        async for i in async_countdown(3):
            print(i)  # 3, 2, 1
    """
    # TODO: use `yield` inside an `async def` (that's the async-generator syntax)
    
    for i in range(n, 0, -1):
        await asyncio.sleep(0.001)
        yield i

class AsyncTimer:
    """An ASYNC context manager with __aenter__ and __aexit__.

    __aenter__ records the start time in self.elapsed and returns self.
    __aexit__ computes the elapsed time (time.monotonic() - start) and
    stores it in self.elapsed as a float, then returns False (don't
    suppress exceptions).

    Usage:
        async with AsyncTimer() as t:
            await asyncio.sleep(0.01)
        t.elapsed  # ~0.01

    Hint: import time at the top of this file.
    """

    def __init__(self):
        self.start = 0.0
        self.elapsed = 0.0

    async def __aenter__(self):
        self.start = time.monotonic()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # TODO: self.elapsed = time.monotonic() - self.start; return False
        self.elapsed = time.monotonic() - self.start
        return False
