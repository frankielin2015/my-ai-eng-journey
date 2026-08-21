"""
Exercise 01 — Syntax Basics
===========================

Welcome! Coming from TS/Java, Python syntax will feel terse and friendly.
Fill in each function body, replacing `raise NotImplementedError`.

Run ONLY this module's tests:
    uv run pytest tests/test_ex01_syntax_basics.py -v

Topics: functions, default args, *args/**kwargs, conditionals, loops,
ternary expressions, tuple unpacking, the walrus operator.
"""
from __future__ import annotations


def add(a: int, b: int) -> int:
    """Return the sum of a and b. (Yes, the gentle warm-up.)"""
    return a + b


def greet(name: str, greeting: str = "Hello") -> str:
    """Return "<greeting>, <name>!" — note the DEFAULT argument value.

    greet("Sam")             -> "Hello, Sam!"
    greet("Sam", "Howdy")    -> "Howdy, Sam!"
    """
    return f"{greeting}, {name}!"


def sum_all(*numbers: int) -> int:
    """Sum any number of positional args using *args. sum_all(1, 2, 3) -> 6."""
    return sum(numbers)
    

def build_profile(**fields) -> dict:
    """Return the keyword args as a dict using **kwargs.

    build_profile(name="Sam", role="staff") -> {"name": "Sam", "role": "staff"}
    """
    return fields


def classify(n: int) -> str:
    """Return "negative", "zero", or "positive" using if/elif/else."""
    if n < 0:
        return "negative"
    elif n == 0:
        return "zero"
    else:
        return "positive"


def abs_or_zero(n: int) -> int:
    """Return abs(n) using a TERNARY expression (the one-line if).

    Hint: `value_if_true if condition else value_if_false`
    """
    return abs(n) if n < 0 else n


def fizzbuzz(n: int) -> list[str]:
    """The classic. Return a list of strings for 1..n inclusive.

    Multiples of 3 -> "Fizz", of 5 -> "Buzz", of both -> "FizzBuzz",
    otherwise the number as a string. fizzbuzz(5) ->
    ["1", "2", "Fizz", "4", "Buzz"]
    """
    result = []
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result


def swap(a, b):
    """Return (b, a). Show off Python's tuple unpacking — no temp var!"""
    x, y = (a, b)
    return (y, x)


def first_big(numbers: list[int], threshold: int) -> int | None:
    """Return the first number strictly greater than threshold, else None.

    Bonus challenge: try using the walrus operator `:=` somewhere.
    """
    for num in numbers:
        if (result := num) > threshold:
            return result
    return None

