"""Reference solutions for week5/query.py.

Import after a self-attempt, e.g.:

    from week5.solutions.query_solution import search_solution

Each function's docstring cites the exercise number it answers.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import psycopg2

# src/ on sys.path so `client` and `week5` resolve when run directly.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from client import make_embedder  # noqa: E402
from week5 import db  # noqa: E402
from week5.solutions import db_solution  # noqa: E402

TOP_K = 3
TEXT_PREVIEW_CHARS = 200
OPERATORS = ("<=>", "<->", "<#>")


def embed_query_solution(query: str) -> list[float]:
    """One-map rule (no TODO): embed the query with the ingest model."""
    response = make_embedder().embeddings.create(
        model=db.EMBEDDING_MODEL,
        input=[query],
    )
    return response.data[0].embedding


def search_solution(
    conn: "psycopg2.extensions.connection",
    query_vector: list[float],
    operator: str = "<=>",
    top_k: int = TOP_K,
) -> list[dict]:
    """Exercises 5 & 6: parameterized operator + correct ranking direction.

    `<=>` and `<->` order ascending and map to `1 - distance`. `<#>` is a
    NEGATIVE inner product: pgvector already negates it, so ascending order is
    still best-first, but similarity is `-distance`.
    """
    assert operator in {"<=>", "<->", "<#>"}
    with conn.cursor() as cur:
        cur.execute(
            f"""
            SELECT id, category, severity, text,
                   embedding {operator} %s::vector AS distance
            FROM tickets
            ORDER BY distance ASC
            LIMIT %s;
            """,
            (query_vector, top_k),
        )
        rows = cur.fetchall()
    flip_sign = operator == "<#>"
    return [
        {
            "id": row[0],
            "category": row[1],
            "severity": row[2],
            "text": row[3],
            "similarity": (-row[4]) if flip_sign else (1.0 - row[4]),
        }
        for row in rows
    ]


def check_drift_warn_solution(conn: "psycopg2.extensions.connection") -> None:
    """Exercise 7: warn (loudly) when DB rows used a different model."""
    drifted = db_solution.check_drift_solution(conn)
    if drifted:
        print(
            "WARNING: embedding-model drift detected — rows were embedded with "
            f"{', '.join(drifted)} but queries use '{db.EMBEDDING_MODEL}'. "
            "Re-run ingest.py before trusting these results.",
            file=sys.stderr,
        )


def run_query_solution(
    query: str, top_k: int = TOP_K, operator: str = "<=>"
) -> None:
    """Full CLI query path: one conn, drift check, embed, search, print."""
    conn = db_solution.get_connection_solution()
    try:
        check_drift_warn_solution(conn)
        query_vector = embed_query_solution(query)
        hits = search_solution(conn, query_vector, operator=operator, top_k=top_k)
    finally:
        conn.close()
    print(f"query: {query}\nmodel: {db.EMBEDDING_MODEL}\noperator: {operator}")
    for i, hit in enumerate(hits, start=1):
        print(
            f"\n{i}. [{hit['similarity']:.3f}] {hit['id']} "
            f"({hit['category']}/{hit['severity']})"
        )
        print(hit["text"][:TEXT_PREVIEW_CHARS])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="pgvector search (reference solution).")
    parser.add_argument("query", nargs="+")
    parser.add_argument("--top-k", type=int, default=TOP_K)
    parser.add_argument("--operator", default="<=>", choices=OPERATORS)
    args = parser.parse_args(argv)
    run_query_solution(" ".join(args.query), top_k=args.top_k, operator=args.operator)
    return 0


if __name__ == "__main__":
    sys.exit(main())
