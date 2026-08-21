"""
Exercise 03 — Data Structures
=============================

The four horsemen: list, tuple, dict, set. Master these and you've got
80% of day-to-day Python.

    uv run pytest tests/test_ex03_data_structures.py -v

Topics: list ops, dict ops (get/setdefault/items), set algebra,
tuples as records, counting, grouping.
"""
from __future__ import annotations
from collections import Counter


def dedupe_keep_order(items: list) -> list:
    """Remove duplicates but KEEP first-seen order.

    dedupe_keep_order([3, 1, 3, 2, 1]) -> [3, 1, 2]
    Hint: a set tracks what you've seen.
    """
    # seen = set()
    # result = []
    # for item in items:
    #     if item not in seen:
    #         result.append(item)
    #         seen.add(item)
    # return result
    return list(dict.fromkeys(items))
        

def merge_dicts(a: dict, b: dict) -> dict:
    """Return a new dict with a and b merged; b wins on key conflicts.

    Hint: Python 3.9+ has the `|` operator for dicts.
    """
    return a | b



def word_count(text: str) -> dict[str, int]:
    """Count occurrences of each whitespace-separated word.

    word_count("a b a") -> {"a": 2, "b": 1}
    Hint: dict.get(key, 0) or collections.Counter.
    """
    # res_dict = {}
    # for word in text.split():
    #     res_dict[word] = res_dict.get(word, 0) + 1
    # return res_dict
    return Counter(text.split())
    

def group_by_parity(numbers: list[int]) -> dict[str, list[int]]:
    """Group numbers into {"even": [...], "odd": [...]} preserving order.

    Hint: dict.setdefault is handy here.
    """
    # result = {}
    # for num in numbers:
    #     key = "even" if num % 2 == 0 else "odd"
    #     result.setdefault(key, []).append(num)
    # return result
    return {
        "even": [n for n in numbers if n % 2 == 0],
        "odd": [n for n in numbers if n % 2 != 0],
    }


def common_elements(a: list, b: list) -> set:
    """Return the set of elements present in BOTH lists (set intersection)."""
    return set(a) & set(b)


def only_in_first(a: list, b: list) -> set:
    """Return the set of elements in a but NOT in b (set difference)."""
    return set(a) - set(b)


def top_n(counts: dict[str, int], n: int) -> list[str]:
    """Return the n keys with the highest values, highest first.

    Ties may break arbitrarily. Hint: sorted(key=..., reverse=True).
    """
    return sorted(counts, key=lambda k : counts[k], reverse=True)[:n]

def invert(mapping: dict) -> dict:
    """Swap keys and values. invert({"a": 1}) -> {1: "a"}.

    Assume values are unique and hashable.
    """
    return { value : key for key , value in mapping.items() }


def flatten(nested: list[list]) -> list:
    """Flatten one level of nesting. flatten([[1, 2], [3]]) -> [1, 2, 3]."""
    return [item for lst in nested for item in lst]
