"""Week 5 deliverable: pgvector semantic search over 12 support tickets.

Pattern (Week 4's semantic search, moved into Postgres):
    embed:   query -> local Ollama (`nomic-embed-text`), SAME model as ingest
    guard:   check for embedding-model drift before trusting the results
    search:  pgvector distance operator, ORDER BY distance, LIMIT top-k
    display: distance -> similarity

pgvector distance operators (the one thing to memorise):
    `<=>`  cosine distance      (0 = identical direction)   ORDER BY ASC
    `<->`  L2 / Euclidean       (0 = identical)             ORDER BY ASC
    `<#>`  NEGATIVE inner product (more negative = more similar) ORDER BY ASC
           -> so similarity must flip sign: -1 * distance, and for `<#>`
              ordering ASC means most similar comes first even though the raw
              inner product is larger. Do not order `<#>` DESC.

Usage:
    uv run python src/week5/query.py "package not arrived" [--top-k 3] [--operator "<=>"]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import psycopg2

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from client import make_embedder

from week5 import db

TOP_K = 3
TEXT_PREVIEW_CHARS = 200
OPERATORS = ("<=>", "<->", "<#>")


def embed_query(query: str) -> list[float]:
    """Embed the query with the SAME model used at ingest (one-map rule).

    Easy win, mirrors Week 4: one text in, one vector out. Uses the shared
    `db.EMBEDDING_MODEL` so the one-map rule cannot drift by typo.
    """
    response = make_embedder().embeddings.create(
        model=db.EMBEDDING_MODEL,
        input=[query],
    )
    return response.data[0].embedding


def search(
    conn: "psycopg2.extensions.connection",
    query_vector: list[float],
    operator: str = "<=>",
    top_k: int = TOP_K,
) -> list[dict]:
    """Exercise 5: Operator (parameterized pgvector distance)
    Concept: `<=>`, `<->`, and `<#>` are three different distance functions;
             the operator is data, so build the SQL around an assert-checked
             parameter instead of copy-pasting three queries.
    Write:   `assert operator in {"<=>", "<->", "<#>"}` first, then SELECT
             `id, category, severity, text` plus
             `embedding <operator> %s::vector AS distance` from `tickets`, passing the
             query vector as a Python list (the adapter is already registered
             by `db.get_connection`). Use a parameter for `LIMIT %s`.
    Verify:  `--operator "<->"` and `--operator "<#>"` both run and return
             rows; an illegal operator trips the assert/crash line.

    Exercise 6: Ranking (ORDER BY direction + similarity conversion)
    Concept: distance and similarity point in opposite directions. The
             `<=>`/`<->` results are sorted ASC and converted with
             `similarity = 1 - distance`; `<#>` is a NEGATIVE inner product,
             so its similarity is `-distance`. Sign trap: because pgvector
             already negates the inner product, `<#>` must ALSO be ordered
             ASC — ordering it DESC (the tempting "bigger inner product is
             better" assumption) silently returns the WORST matches first.
    Write:   ORDER BY `distance ASC` for all three operators, then build
             result dicts with `similarity = 1.0 - row[4]` for `<=>`/`<->`
             and `similarity = -row[4]` for `<#>`.
    Verify:  The top hit for "package not arrived" is a shipping ticket and
             its similarity is the largest of the three printed scores; for
             `<#>` a DESC ordering would visibly invert the ranking.
    """
    assert operator in {"<=>", "<->", "<#>"}, f"unknown operator: {operator}"
    select_sql = f"""SELECT id, category, severity, text, embedding {operator} %s::vector AS distance 
    FROM tickets ORDER BY distance ASC LIMIT %s"""
    with conn.cursor() as cur:
        cur.execute(select_sql, (query_vector, top_k))
        rows = cur.fetchall()
    hits = [
        {
            "id": row[0],
            "category": row[1],
            "severity": row[2],
            "text": row[3],
            "similarity": -row[4] if operator == "<#>" else 1.0 - row[4]
        }
        for row in rows
    ]
    return hits
    


def check_drift_warn(conn: "psycopg2.extensions.connection") -> None:
    """Exercise 7: check_drift_warn (embedding-model drift)
    Concept: Vectors from different embedding models are not comparable, so
             querying a table whose rows were embedded with another model is
             silently wrong. Detect it cheaply at query time.
    Write:   Call `db.check_drift(conn)` (already implemented for you — study
             its DISTINCT query). If it returns any model names, print a clear
             WARNING naming those models and `db.EMBEDDING_MODEL`; otherwise
             stay silent so normal runs are quiet.
    Verify:  Manually `UPDATE tickets SET embedded_with = 'other-model' WHERE
             id = 'T-001'`, run a query, and see the warning; restore the row.
    """
    raise NotImplementedError(
        "Exercise 7: implement check_drift_warn(conn) on top of db.check_drift."
    )


def run_query(query: str, top_k: int = TOP_K, operator: str = "<=>") -> None:
    """Query command: open conn -> drift check -> embed -> search -> print.

    Opens ONE connection and closes it explicitly in a `finally` (a `with
    conn:` would only end the transaction, not the socket). Drift is checked
    BEFORE embedding so the warning appears even if the query itself fails.
    """
    conn = db.get_connection()
    try:
        check_drift_warn(conn)
        query_vector = embed_query(query)
        hits = search(conn, query_vector, operator=operator, top_k=top_k)
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
    parser = argparse.ArgumentParser(description="pgvector search over support tickets.")
    parser.add_argument("query", nargs="+", help="natural-language query text")
    parser.add_argument("--top-k", type=int, default=TOP_K, help="number of hits (default 3)")
    parser.add_argument(
        "--operator",
        default="<=>",
        choices=OPERATORS,
        help="pgvector distance operator (default <=> cosine)",
    )
    args = parser.parse_args(argv)
    run_query(" ".join(args.query), top_k=args.top_k, operator=args.operator)
    return 0


if __name__ == "__main__":
    sys.exit(main())
