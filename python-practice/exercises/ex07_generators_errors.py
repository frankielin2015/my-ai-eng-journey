"""
Exercise 07 — Generators, Iterators & Error Handling
====================================================

Generators are everywhere in Python (and AI data pipelines): lazy,
memory-efficient streams. Plus exceptions — Python's preferred control
flow for "exceptional" cases.

    uv run pytest tests/test_ex07_generators_errors.py -v

Topics: yield, generator expressions, itertools-style logic, try/except/
else/finally, raising, custom exceptions, context managers.
"""
from __future__ import annotations

from contextlib import contextmanager
from itertools import islice


def countdown(n: int):
    """A GENERATOR that yields n, n-1, ..., 1 (use `yield`).

    list(countdown(3)) -> [3, 2, 1]
    """
    return (i for i in range(n, 0, -1))
    # for i in range(n, 0, -1):
    #     yield i


def take(iterable, n: int) -> list:
    """Return the first n items from any iterable as a list.

    Works on infinite generators too! take(countdown(100), 2) -> [100, 99]
    """
    # result = []
    # for i in iterable:
    #     if len(result) >= n:
    #         break
    #     result.append(i)
    # return result
    return list(islice(iterable, n))


def fibonacci():
    """An INFINITE generator of Fibonacci numbers: 0, 1, 1, 2, 3, 5, ...

    Use with take(): take(fibonacci(), 5) -> [0, 1, 1, 2, 3]
    """
    a, b = 0, 1
    while True:
        yield a
        a , b = b, a + b


def running_total(numbers):
    """Yield the cumulative sum so far for each number.

    list(running_total([1, 2, 3])) -> [1, 3, 6]
    """
    # A GENERATOR (matches the docstring's "Yield"): keep a running
    # `total` as state and yield it each step -- lazy, works on streams.
    # Pro tip for real code: itertools.accumulate(numbers) does exactly this.
    # total = 0
    # for n in numbers:
    #     total += n
    #     yield total
    total = 0
    return ((total := total + x) for x in numbers)



def safe_divide(a: float, b: float) -> float | None:
    """Return a / b, but return None on ZeroDivisionError.

    Use try/except. safe_divide(10, 2) -> 5.0 ; safe_divide(1, 0) -> None
    """
    try:
        return a / b
    except ZeroDivisionError:
        return None



def parse_int(value: str, default: int = 0) -> int:
    """Return int(value), or `default` if it can't be parsed (ValueError)."""
    try:
        return int(value)
    except ValueError:
        return default


class WithdrawalError(Exception):
    """A CUSTOM exception. Nothing to implement — just subclassing Exception."""


def withdraw(balance: int, amount: int) -> int:
    """Return balance - amount, but raise WithdrawalError (with message
    "Insufficient funds") if amount > balance.
    """
    if balance >= amount:
        return balance - amount
    else:
        raise WithdrawalError("Insufficient funds")

@contextmanager
def track_calls(log: list):
    """A context manager (using @contextmanager) that appends "enter" to
    `log` on entry and "exit" on exit (even if an exception occurs).

    Usage:
        log = []
        with track_calls(log):
            ...
        # log == ["enter", "exit"]

    Hint: use try/finally around the `yield`.
    """
    log.append("enter")
    try:
        yield
    finally:
        log.append("exit")
    
