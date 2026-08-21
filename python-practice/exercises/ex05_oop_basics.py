"""
Exercise 05 — OOP Basics
========================

Classes, __init__, instance vs class attributes, methods. Coming from
Java this is familiar — but note: no `new`, explicit `self`, and far
less ceremony.

    uv run pytest tests/test_ex05_oop_basics.py -v
"""
from __future__ import annotations


class Counter:
    """A simple counter.

    - __init__(start=0): store the starting value on self.value
    - increment(by=1): add `by` to self.value, return new value
    - reset(): set self.value back to 0
    """

    def __init__(self, start: int = 0) -> None:
        self.value = start

    def increment(self, by: int = 1) -> int:
        self.value += by
        return self.value

    def reset(self) -> None:
        self.value = 0


class BankAccount:
    """A tiny bank account.

    - __init__(owner, balance=0): store owner and balance
    - deposit(amount): add to balance; raise ValueError if amount <= 0
    - withdraw(amount): subtract; raise ValueError if amount <= 0 OR
      if amount > balance (message: "Insufficient funds")
    - __str__: return "<owner>: $<balance>"  e.g. "Sam: $100"
    """

    def __init__(self, owner: str, balance: int = 0) -> None:
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: int) -> None:
        if amount > 0:
            self.balance += amount
        else:
            raise ValueError

    def withdraw(self, amount: int) -> None:
        if self.balance >= amount:
            self.balance -= amount
        else:
            raise ValueError

    def __str__(self) -> str:
        return f"{self.owner}: ${self.balance}"


class Circle:
    """Geometry with a CLASS attribute.

    - pi: a class attribute equal to 3.14159 (shared across instances)
    - __init__(radius): store radius
    - area(): return pi * radius ** 2
    - circumference(): return 2 * pi * radius
    """

    pi = 3.14159

    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        return Circle.pi * self.radius ** 2

    def circumference(self) -> float:
        return 2 * self.pi * self.radius
