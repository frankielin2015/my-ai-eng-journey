"""Week 4 deliverable: semantic search over your python-practice notes.

Pattern (from the Wikipedia embeddings cookbook, adapted):
    collect: glob python-practice/*.md      (one file = one chunk)
    embed:   batch through local Ollama, verify pairing order
    store:   JSON file of (filename, text, vector)
    search:  embed query (same model) -> cosine against all -> top-k

Usage:
    uv run python src/week4/semantic_search.py index    # embed corpus, save index
    uv run python src/week4/semantic_search.py search "your query"  # top-k results
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from client import make_embedder

CORPUS_DIR = Path(__file__).resolve().parent.parent.parent.parent / "python-practice"
INDEX_PATH = Path(__file__).resolve().parent / "semantic_index.json"
EMBEDDING_MODEL = "nomic-embed-text"
TOP_K = 3


def load_corpus() -> list[dict]:
    """Collect: read every .md file in python-practice/ as {"name", "text"}."""
    return [{"name": p.name, "text": p.read_text(encoding="utf-8")} for p in sorted(CORPUS_DIR.glob("*.md"))]


def embed_documents(docs: list[dict]) -> list[dict]:
    """Embed: attach a vector to each doc, batched.

    Mutates docs in place, adding "vector" to each dict.

    Pairing strategy: POSITIONAL — data[i] belongs to docs[i].
    Safe because the asserts below verify the API returned vectors
    in input order (actual position i == record's claimed index).
    If an API ever returned out-of-order BY DESIGN, switch to using
    record.index as the lookup key instead of position (and drop assert 2).
    """
    response = make_embedder().embeddings.create(
        model=EMBEDDING_MODEL,
        input=[doc["text"] for doc in docs],
    )
    # Assert 1: truncation check — one record per input text.
    assert len(response.data) == len(docs)
    # Assert 2: pairing check — record at position i claims to be for input i.
    for i, record in enumerate(response.data):
        assert i == record.index
        docs[i]["vector"] = record.embedding
    return docs


def embed_query(query: str) -> list[float]:
    """Embed the query with the SAME model (one-map rule)."""
    response = make_embedder().embeddings.create(
        model=EMBEDDING_MODEL,
        input=[query],
    )
    return response.data[0].embedding


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Cosine similarity: dot(a,b) / (||a|| * ||b||).

    Measures direction-only similarity in [-1, 1]; length-independent.
    Hand-written deliberately (fluency rep) — production code would use
    numpy or a library helper. Returns 0.0 on zero vectors (defensive).
    """
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x ** 2 for x in a))
    norm_b = math.sqrt(sum(y ** 2 for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def search(query: str, index: list[dict]) -> list[dict]:
    """Score every doc against the query, return top_k as
    [{"name": ..., "text": ..., "score": ...}] sorted by score desc.

    Pure: builds a new list, never mutates the index (so callers can
    safely run multiple queries over one loaded index).
    """
    query_vector = embed_query(query)
    scored = [
        {
            "name": doc["name"],
            "text": doc["text"],
            "score": cosine_similarity(query_vector, doc["vector"]),
        }
        for doc in index
    ]
    return sorted(scored, key=lambda r: r["score"], reverse=True)[:TOP_K]


def build_index() -> None:
    """Index command: corpus -> embed -> save JSON."""
    docs = embed_documents(load_corpus())
    INDEX_PATH.write_text(json.dumps(docs))
    print(f"indexed {len(docs)} docs -> {INDEX_PATH}")


def run_search(query: str) -> None:
    """Search command: load JSON -> search -> print results."""
    index = json.loads(INDEX_PATH.read_text())
    for hit in search(query, index):
        print(f"\n[{hit['score']:.3f}] {hit['name']}")
        print(hit["text"][:300])


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "index":
        build_index()
    elif len(sys.argv) >= 3 and sys.argv[1] == "search":
        run_search(" ".join(sys.argv[2:]))
    else:
        print(__doc__)