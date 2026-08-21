"""
Exercise 06 — OOP Advanced
==========================

The stuff that makes Python OOP feel different from Java: inheritance &
super(), dunder methods for operator overloading, @property, @dataclass,
@classmethod / @staticmethod.

    uv run pytest tests/test_ex06_oop_advanced.py -v
"""
from __future__ import annotations

from dataclasses import dataclass


class Animal:
    """Base class.

    - __init__(name): store name
    - speak(): return f"{name} makes a sound"
    """

    def __init__(self, name: str) -> None:
        self.name = name

    def speak(self) -> str:
        return f"{self.name} makes a sound"


class Dog(Animal):
    """Subclass of Animal.

    - speak(): override to return f"{name} says Woof"  (use self.name)
    - fetch(): return f"{name} fetches the ball"
    Reuse the parent __init__ (don't redefine it).
    """

    def speak(self) -> str:
        return f"{self.name} says Woof"

    def fetch(self) -> str:
        return f"{self.name} fetches the ball"


class Vector:
    """A 2D vector demonstrating dunder methods.

    - __init__(x, y): store coords
    - __add__(other): return a new Vector with summed components
    - __eq__(other): equal when both components match
    - __repr__: return "Vector(x, y)"  e.g. "Vector(1, 2)"
    - __abs__: return the magnitude sqrt(x**2 + y**2)
    """

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other: object) -> bool:
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def __abs__(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5


class Temperature:
    """Demonstrates @property (computed/validated attributes).

    - __init__(celsius): store via the setter below
    - celsius: a @property with getter + setter; setter raises ValueError
      if value < -273.15 (absolute zero)
    - fahrenheit: a read-only @property computed as celsius * 9/5 + 32
    """

    def __init__(self, celsius: float) -> None:
        # Assigning to self.celsius here goes THROUGH the setter below,
        # so validation happens even at construction time. Nice reuse.
        self.celsius = celsius

    @property
    def celsius(self) -> float:
        # GETTER: runs when you read `t.celsius`. Hands back the
        # real stored value from the "private" attribute.
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        # SETTER: runs when you write `t.celsius = value`.
        # Guard clause first: reject anything below absolute zero.
        if value < -273.15:
            raise ValueError("Below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        # Read-only computed property: no setter defined, so you
        # can READ t.fahrenheit but can't assign to it.
        return self.celsius * 9 / 5 + 32


@dataclass
class Point:
    """Fill in the fields so a Point has integer x and y.

    @dataclass auto-generates __init__, __repr__, and __eq__ for you.
    Replace the `pass` with two annotated fields: x: int and y: int.
    Then implement manhattan() to return abs(x) + abs(y).
    """

    x: int
    y: int

    def manhattan(self) -> int:
        # Distance from origin measured in grid steps (no diagonals):
        # how far along x PLUS how far along y, ignoring sign.
        return abs(self.x) + abs(self.y)


class MathUtils:
    """Demonstrates @staticmethod and @classmethod.

    - add (staticmethod): return a + b, no self/cls needed
    - description (classmethod): return f"This is {cls.__name__}"
    """

    @staticmethod
    def add(a: int, b: int) -> int:
        # No self, no cls -- just a plain function living in the class.
        return a + b

    @classmethod
    def description(cls) -> str:
        # cls IS the class (MathUtils). __name__ is its name as a string.
        return f"This is {cls.__name__}"
