"""
Exercise 02 — Built-in Functions
================================

Python's standard library has a LOT of built-ins that replace loops you'd
write by hand in Java. Lean on them — it's the Pythonic way.

    uv run pytest tests/test_ex02_builtins.py -v

Topics: len, sum, min, max, sorted, reversed, enumerate, zip, map,
filter, any, all, abs, round, range.
"""
from __future__ import annotations


def total_and_count(numbers: list[int]) -> tuple[int, int]:
    """Return (sum, count) using sum() and len()."""
    return (sum(numbers), len(numbers))


def min_max(numbers: list[int]) -> tuple[int, int]:
    """Return (smallest, largest) using min() and max()."""
    return (min(numbers), max(numbers))


def sort_desc(numbers: list[int]) -> list[int]:
    """Return a NEW list sorted high-to-low using sorted(..., reverse=True)."""
    return sorted(numbers, reverse=True)


def sort_by_length(words: list[str]) -> list[str]:
    """Sort words by length (shortest first) using sorted(key=...)."""
    return sorted(words, key=len)


def index_each(items: list[str]) -> list[tuple[int, str]]:
    """Return [(0, item0), (1, item1), ...] using enumerate()."""
    return list(enumerate(items))


def pair_up(keys: list[str], values: list[int]) -> list[tuple[str, int]]:
    """Pair keys with values using zip(). pair_up(["a"], [1]) -> [("a", 1)]."""
    return list(zip(keys, values))


def squares(numbers: list[int]) -> list[int]:
    """Return each number squared. Use map() (or a comprehension if you prefer)."""
    # return list(map(lambda x : x ** 2, numbers))
    return [x ** 2 for x in numbers]

def only_even(numbers: list[int]) -> list[int]:
    """Return only the even numbers using filter()."""
    # return list(filter(lambda num : num % 2 == 0, numbers))
    return [ x for x in numbers if x % 2 == 0 ]


def has_any_negative(numbers: list[int]) -> bool:
    """Return True if ANY number is negative, using any()."""
    return any(n < 0 for n in numbers)


def all_positive(numbers: list[int]) -> bool:
    """Return True if ALL numbers are positive, using all()."""
    return all(n > 0 for n in numbers)


def rounded(values: list[float], ndigits: int = 2) -> list[float]:
    """Round each value to ndigits using round()."""
    return [round(x, ndigits) for x in values]
