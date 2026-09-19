"""Week 5 deliverable: text chunking strategies for RAG.

Retrieval quality is bounded by how you split documents. Three strategies,
from crude to context-aware:

    fixed:      hard cut every `size` chars with `overlap` chars of carry-over.
                Cheap, but slices mid-sentence/mid-word.
    sentences:  greedily pack whole sentences up to `size` chars. Never cuts a
                sentence in half.
    recursive:  split on the biggest separator that yields pieces <= `size`
                (paragraphs -> sentences -> words), recursing only where a
                piece is still too long. The common production default.

Exercises 8 (all three functions) live here; exercises 9 is the bake-off that
compares them on `policy.md`. Constants like the embedding model are NOT
duplicated here — import `db.EMBEDDING_MODEL` when you embed these chunks.
"""
from __future__ import annotations

import re

SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+")


def split_sentences(text: str) -> list[str]:
    """Split `text` into sentences on whitespace after `.`, `!`, or `?`.

    Provided utility (not a TODO): the regex is fiddly and not the lesson.
    Returns stripped, non-empty sentences in document order. This is the
    building block `chunk_sentences` and `chunk_recursive` pack into chunks.
    """
    return [s.strip() for s in SENTENCE_BOUNDARY.split(text.strip()) if s.strip()]


def chunk_fixed(text: str, size: int = 200, overlap: int = 40) -> list[str]:
    """Exercise 8: chunk_fixed (fixed-size window)
    Concept: The simplest splitter. A sliding window of `size` characters
             advances by `size - overlap`, so `overlap` characters of context
             survive the boundary and an answer spanning a cut is still
             retrievable.
    Write:   Validate `0 <= overlap < size`, then walk a start index from 0 to
             `len(text)` in steps of `size - overlap`, appending
             `text[start:start + size]`. Stop as soon as the window reaches the
             end, and drop empty/whitespace-only chunks.
    Verify:  For a 1000-char text with size=200, overlap=40 the chunk count is
             `ceil((1000 - 40) / (200 - 40)) = 6`; the first 40 chars of chunk
             n+1 equal the last 40 chars of chunk n.
    """
    raise NotImplementedError("Exercise 8: implement chunk_fixed(text, size, overlap).")


def chunk_sentences(text: str, size: int = 200) -> list[str]:
    """Exercise 8: chunk_sentences (sentence-packed)
    Concept: Respect sentence boundaries so no chunk is a fragment. Greedily
             append whole sentences until the next one would push the chunk
             over `size` characters, then start a new chunk.
    Write:   Use `split_sentences(text)`. Keep a running buffer; for each
             sentence, if the buffer is non-empty and
             `len(buffer) + 1 + len(sentence) > size`, flush the buffer and
             start fresh. Append the sentence and flush whatever remains at
             the end. A single sentence longer than `size` becomes its own
             (oversized) chunk rather than being split.
    Verify:  Every returned chunk (except any oversized single sentence) is
             `<= size` chars, and concatenating the chunks with a space
             reproduces the original sentence sequence.
    """
    raise NotImplementedError("Exercise 8: implement chunk_sentences(text, size).")


def chunk_recursive(text: str, size: int = 200, overlap: int = 40) -> list[str]:
    """Exercise 8: chunk_recursive (hierarchical splitter)
    Concept: Try the most semantic separator first and only fall back when a
             piece is still too big. This keeps paragraphs intact when they
             fit and degrades gracefully for wall-of-text input.
    Write:   Implement a recursive helper over the separator ladder
             `["\\n\\n", "\\n", ". ", " "]`. If `len(piece) <= size`, keep it.
             Otherwise split on the current separator; if the separator is not
             found in the piece, move to the next one. Merge small pieces back
             up to `size` so the output is not a spray of one-sentence chunks.
             Apply `overlap` only at the final merge, exactly like
             `chunk_fixed`.
    Verify:  On `policy.md`, each chunk is `<= size` chars, paragraph headings
             stay attached to their paragraph, and the number of chunks is
             smaller than `chunk_fixed`'s for the same size.
    """
    raise NotImplementedError("Exercise 8: implement chunk_recursive(text, size, overlap).")
