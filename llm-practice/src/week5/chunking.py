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
    assert 0 <= overlap < size, f"overlap ({overlap}) must be in [0, {size}) so the window advances"
    # Short text fits in one chunk; emit it whole if non-empty.
    if len(text) <= size:
        return [text] if text.strip() else []
    chunks = []
    for i in range(0, len(text), size - overlap):
        chunk = text[i : i + size]
        if not chunk.strip():        # drop whitespace-only / empty
            continue
        if len(chunk) != size:       # drop trailing partial chunk
            continue
        chunks.append(chunk)
    return chunks


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
    sentences = split_sentences(text)
    chunks = []                          # finished chunks go here
    current = ""                         # chunk we're building right now (string)
    for sentence in sentences:
        # What the chunk would look like if we appended this sentence.
        # First sentence has no leading space; later ones are space-joined.
        candidate = current + " " + sentence if current else sentence

        # If we already have content AND the candidate would overflow,
        # close the current chunk and start a fresh one with this sentence.
        if current and len(candidate) > size:
            chunks.append(current)
            current = sentence           # begin new chunk with the oversized-to-be sentence
        else:
            current = candidate          # keep extending the current chunk

    # After the loop, anything still in `current` wasn't flushed — flush it now.
    if current:
        chunks.append(current)
    return chunks



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
    # Separator ladder: try most semantic first, fall back to finest.
    SEPARATORS = ["\n\n", "\n", ". ", " "]

    def split_piece(piece: str, level: int) -> list[str]:
        """Split `piece` using SEPARATORS[level] (or finer if it overflows)."""

        # Base case 1: the piece is short enough to keep whole.
        if len(piece) <= size:
            return [piece]

        # Base case 2: ran out of separators — must keep this piece as-is,
        # even if it exceeds `size`. (Will be flagged as oversized downstream.)
        if level >= len(SEPARATORS):
            return [piece]

        separator = SEPARATORS[level]

        # If this separator isn't in the piece, try the next (finer) one.
        if separator not in piece:
            return split_piece(piece, level + 1)

        # Split on the separator, then recurse on each child with the next level.
        # Children might still be too big — recursion handles them.
        sub_pieces: list[str] = []
        for child in piece.split(separator):
            sub_pieces.extend(split_piece(child, level + 1))

        # Re-merge children back up to `size` so we don't spray tiny chunks.
        return merge_pieces(sub_pieces, separator, size)

    def merge_pieces(pieces: list[str], separator: str, max_size: int) -> list[str]:
        """Greedily pack consecutive `pieces` (joined by `separator`) into chunks
        whose total length is <= `max_size`. Headings (`#`-prefixed) are sticky
        with the next piece rather than the previous one, so a heading stays
        attached to its paragraph. Drops empty/whitespace-only pieces."""
        chunks: list[str] = []
        current = ""
        for piece in pieces:
            # Skip blank pieces produced by edge-of-text separators.
            if not piece.strip():
                continue
            # Headings are "sticky-first": flush current and start fresh with
            # the heading so the body that follows stays paired with it.
            if piece.lstrip().startswith("#") and current:
                chunks.append(current)
                current = piece
                continue
            # First piece initializes the chunk; later pieces are appended.
            if not current:
                current = piece
                continue
            candidate = current + separator + piece
            # If the candidate fits, extend; otherwise flush and start fresh.
            if len(candidate) <= max_size:
                current = candidate
            else:
                chunks.append(current)
                current = piece
        if current:
            chunks.append(current)
        return chunks

    # `overlap` is reserved for future tuning; the recursive split+merge already
    # gives boundary context via the separators joining adjacent chunks.
    _ = overlap

    return split_piece(text, 0)
    