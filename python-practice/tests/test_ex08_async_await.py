import asyncio
import time

import pytest

from exercises.ex08_async_await import (
    AsyncTimer,
    async_add,
    async_countdown,
    async_identity,
    call_an_async_function,
    cancel_slow_call,
    gather_with_errors,
    run_concurrently,
    run_sequentially,
    run_with_create_task,
)


# ---------------------------------------------------------------------------
# Part 1 — Coroutines
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_async_identity():
    assert await async_identity(42) == 42
    assert await async_identity("hello") == "hello"


@pytest.mark.asyncio
async def test_async_add():
    assert await async_add(20, 22) == 42
    assert await async_add(0, 0) == 0
    assert await async_add(-5, 5) == 0


@pytest.mark.asyncio
async def test_call_an_async_function():
    assert await call_an_async_function(21) == 42
    assert await call_an_async_function(0) == 0


# ---------------------------------------------------------------------------
# Part 2 — Concurrency: gather & create_task
# ---------------------------------------------------------------------------

def elapsed_seconds(coro):
    """Run a coroutine and return (result, elapsed_seconds)."""
    start = time.monotonic()
    result = asyncio.run(coro())
    elapsed = time.monotonic() - start
    return result, elapsed


@pytest.mark.asyncio
async def test_run_sequentially():
    results = await run_sequentially()
    assert results == ["a done", "b done", "c done"]


def test_run_sequentially_is_actually_sequential():
    results, elapsed = elapsed_seconds(run_sequentially)
    assert results == ["a done", "b done", "c done"]
    # Sequential means we wait for all three 0.01s sleeps in series
    assert elapsed >= 0.03


@pytest.mark.asyncio
async def test_run_concurrently():
    results = await run_concurrently()
    assert results == ["a done", "b done", "c done"]


def test_run_concurrently_is_actually_concurrent():
    results, elapsed = elapsed_seconds(run_concurrently)
    assert results == ["a done", "b done", "c done"]
    # Concurrent means wall-clock ~= the longest single sleep
    assert elapsed < 0.025


@pytest.mark.asyncio
async def test_run_with_create_task():
    results = await run_with_create_task()
    assert results == ["a done", "b done", "c done"]


def test_run_with_create_task_is_concurrent():
    results, elapsed = elapsed_seconds(run_with_create_task)
    assert results == ["a done", "b done", "c done"]
    assert elapsed < 0.025


# ---------------------------------------------------------------------------
# Part 3 — Timeouts, cancellation, error handling
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_cancel_slow_call():
    result = await cancel_slow_call()
    assert result == "cancelled"


@pytest.mark.asyncio
async def test_gather_with_errors():
    results = await gather_with_errors()
    assert results[0] == "ok1 done"
    assert isinstance(results[1], ValueError)
    assert str(results[1]) == "boom"
    assert results[2] == "ok2 done"


# ---------------------------------------------------------------------------
# Part 4 — Async generators & async context managers
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_async_countdown():
    collected = []
    async for i in async_countdown(5):
        collected.append(i)
    assert collected == [5, 4, 3, 2, 1]


@pytest.mark.asyncio
async def test_async_countdown_empty():
    collected = []
    async for i in async_countdown(0):
        collected.append(i)
    assert collected == []


@pytest.mark.asyncio
async def test_async_timer():
    async with AsyncTimer() as t:
        await asyncio.sleep(0.02)
    assert isinstance(t.elapsed, float)
    # Should be at least the sleep time, not absurdly long
    assert 0.015 <= t.elapsed < 0.5


@pytest.mark.asyncio
async def test_async_timer_doesnt_swallow_exceptions():
    with pytest.raises(RuntimeError):
        async with AsyncTimer():
            raise RuntimeError("boom")
