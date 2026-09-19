"""Reference solutions for week5/chunking.py.

Import after a self-attempt, e.g.:

    from week5.solutions.chunking_solution import chunk_recursive_solution

Each function's docstring cites the exercise number it answers.
"""
from __future__ import annotations

import sys
from pathlib import Path

# src/ on sys.path so `week5` resolves when run directly.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from week5 import chunking  # noqa: E402

SEPARATORS = ["\n\n", "\n", ". ", " "]


def chunk_fixed_solution(text: str, size: int = 200, overlap: int = 40) -> list[str]:
    """Exercise 8: sliding window of `size` chars advancing by size - overlap."""
    assert 0 <= overlap < size, "overlap must satisfy 0 <= overlap < size"
    step = size - overlap
    chunks: list[str] = []
    for start in range(0, len(text), step):
        window = text[start : start + size]
        if not window.strip():
            break
        chunks.append(window)
        if start + size >= len(text):
            break
    return chunks


def chunk_sentences_solution(text: str, size: int = 200) -> list[str]:
    """Exercise 8: greedily pack whole sentences up to `size` chars."""
    chunks: list[str] = []
    buffer = ""
    for sentence in chunking.split_sentences(text):
        candidate = f"{buffer} {sentence}".strip()
        if buffer and len(candidate) > size:
            chunks.append(buffer)
            buffer = sentence
        else:
            buffer = candidate
    if buffer:
        chunks.append(buffer)
    return chunks


def _recursive_pieces(text: str, size: int, separators: list[str]) -> list[str]:
    """Split `text` into pieces <= size on the first separator that fits."""
    if len(text) <= size:
        return [text]
    if not separators:
        return [text[i : i + size] for i in range(0, len(text), size)]
    separator = separators[0]
    if separator not in text:
        return _recursive_pieces(text, size, separators[1:])
    pieces: list[str] = []
    for part in text.split(separator):
        pieces.extend(_recursive_pieces(part, size, separators[1:]))
    return pieces


def _merge_pieces(pieces: list[str], size: int, overlap: int) -> list[str]:
    """Merge small pieces back up to `size`, carrying `overlap` chars across."""
    chunks: list[str] = []
    buffer = ""
    for raw in pieces:
        piece = raw.strip()
        if not piece:
            continue
        if buffer and len(buffer) + 1 + len(piece) > size:
            chunks.append(buffer)
            carry = buffer[-overlap:] if overlap else ""
            buffer = f"{carry} {piece}".strip() if carry else piece
        else:
            buffer = f"{buffer} {piece}".strip()
    if buffer:
        chunks.append(buffer)
    return chunks


def chunk_recursive_solution(text: str, size: int = 200, overlap: int = 40) -> list[str]:
    """Exercise 8: paragraphs -> sentences -> words, then merge with overlap."""
    assert 0 <= overlap < size, "overlap must satisfy 0 <= overlap < size"
    pieces = _recursive_pieces(text, size, SEPARATORS)
    return _merge_pieces(pieces, size, overlap)
