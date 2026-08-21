"""
Exercise 04 — Comprehensions & Strings
======================================

Comprehensions are Python's superpower — they replace map/filter loops
with one readable line. Plus a dose of string manipulation.

    uv run pytest tests/test_ex04_comprehensions.py -v

Topics: list/dict/set comprehensions, conditional comprehensions,
nested comprehensions, str methods (split, join, strip, etc.), slicing.
"""
from __future__ import annotations


def squares_comp(n: int) -> list[int]:
    """Return [0, 1, 4, 9, ...] for 0..n-1 using a LIST comprehension."""
    return [x ** 2 for x in range(n)]


def even_squares(n: int) -> list[int]:
    """Squares of even numbers in 0..n-1 using a comprehension WITH a filter.

    even_squares(6) -> [0, 4, 16]  (0^2, 2^2, 4^2)
    """
    return [x ** 2 for x in range(n) if x % 2 == 0]


def lengths_by_word(words: list[str]) -> dict[str, int]:
    """{word: len(word)} using a DICT comprehension."""
    return {word : len(word) for word in words }


def unique_first_letters(words: list[str]) -> set[str]:
    """Set of first letters using a SET comprehension."""
    return { word[0] for word in words }

def grid(rows: int, cols: int) -> list[list[int]]:
    """Build a rows x cols grid where cell[r][c] == r * cols + c.

    grid(2, 3) -> [[0, 1, 2], [3, 4, 5]]  (nested comprehension)
    """
    return [[row * cols + col for col in range(cols)] for row in range(rows)]


def to_snake_case(text: str) -> str:
    """Convert "Hello World Foo" -> "hello_world_foo".

    Hint: .lower(), .split(), "_".join(...).
    """
    return "_".join(text.lower().split())


def normalize(text: str) -> str:
    """Strip surrounding whitespace and collapse internal runs of spaces.

    normalize("  hello   world  ") -> "hello world"
    Hint: .split() with no args splits on any run of whitespace.
    """
    return " ".join(text.split())


def reverse_words(sentence: str) -> str:
    """Reverse the ORDER of words. "the quick fox" -> "fox quick the"."""

    return " ".join(sentence.split()[::-1])


def is_palindrome(text: str) -> bool:
    """Case-insensitive palindrome check, ignoring spaces.

    is_palindrome("Race car") -> True
    Hint: slicing [::-1] reverses a sequence.
    """
    return text.lower().replace(" ", "") == text.replace(" ", "").lower()[::-1]


def initials(full_name: str) -> str:
    """Return uppercase initials. "ada lovelace" -> "AL"."""
    # res = ""
    # for word in full_name.split():
    #     res += word[0].upper()
    # return res

    return "".join(word[0].upper() for word in full_name.split())
