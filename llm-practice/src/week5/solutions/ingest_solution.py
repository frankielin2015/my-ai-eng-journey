"""Reference solutions for week5/ingest.py.

Import after a self-attempt, e.g.:

    from week5.solutions.ingest_solution import main_solution

Each function's docstring cites the exercise number it answers.
"""
from __future__ import annotations

import json
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

CORPUS_PATH = Path(__file__).resolve().parents[2] / "midterm" / "tickets_corpus.json"


def load_corpus_solution() -> list[dict]:
    """Exercise 4 (support): read the ticket corpus."""
    return json.loads(CORPUS_PATH.read_text(encoding="utf-8"))


def embed_tickets_solution(tickets: list[dict], batch_size: int = 4) -> list[dict]:
    """Exercise 4: batched embedding with positional pairing asserts."""
    for start in range(0, len(tickets), batch_size):
        batch = tickets[start : start + batch_size]
        response = make_embedder().embeddings.create(
            model=db.EMBEDDING_MODEL,
            input=[ticket["text"] for ticket in batch],
        )
        # Assert 1: truncation check — one record per input text.
        assert len(response.data) == len(batch)
        # Assert 2: pairing check — record at position i claims input i.
        for i, record in enumerate(response.data):
            assert i == record.index
            batch[i]["embedding"] = record.embedding
    return tickets


def upsert_tickets_solution(
    conn: "psycopg2.extensions.connection", tickets: list[dict]
) -> None:
    """Exercise 4: idempotent UPSERT; no commit here (caller commits once)."""
    with conn.cursor() as cur:
        for ticket in tickets:
            cur.execute(
                """
                INSERT INTO tickets (id, text, category, severity, embedding, embedded_with)
                VALUES (%s, %s, %s, %s, %s::vector, %s)
                ON CONFLICT (id) DO UPDATE SET
                    text = EXCLUDED.text,
                    category = EXCLUDED.category,
                    severity = EXCLUDED.severity,
                    embedding = EXCLUDED.embedding,
                    embedded_with = EXCLUDED.embedded_with;
                """,
                (
                    ticket["id"],
                    ticket["text"],
                    ticket["category"],
                    ticket["severity"],
                    ticket["embedding"],
                    db.EMBEDDING_MODEL,
                ),
            )


def main_solution() -> int:
    """Exercise 4: single-connection flow — open, schema, embed, upsert,
    commit once, close. `len(tickets)` is reused, and `load_corpus` is called
    exactly once."""
    tickets = load_corpus_solution()
    conn = db_solution.get_connection_solution()
    try:
        print("connection ok")
        db_solution.init_schema_solution(conn)
        print(f"embedding {len(tickets)} tickets")
        embed_tickets_solution(tickets)
        upsert_tickets_solution(conn, tickets)
        conn.commit()
        print("write ok")
    except Exception as exc:  # noqa: BLE001
        conn.rollback()
        print(f"ingest failed: {exc}", file=sys.stderr)
        return 1
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main_solution())
