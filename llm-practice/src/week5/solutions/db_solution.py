"""Reference solutions for week5/db.py.

Import after a self-attempt, e.g.:

    from week5.solutions.db_solution import init_schema_solution

Each function's docstring cites the exercise number it answers so you can map
it back to the TODO in db.py.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import psycopg2

# src/ on sys.path so `from week5 import db` resolves when run directly.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from week5 import db  # noqa: E402


def get_connection_solution() -> "psycopg2.extensions.connection":
    """Exercise 2: connection + pgvector adapter.

    Mirrors db.get_connection: register_vector must run per connection so a
    Python list can be bound to a `vector` column. Caller closes.
    """
    import psycopg2
    from pgvector.psycopg2 import register_vector

    conn = psycopg2.connect(**db.CONNECTION_PARAMS)
    register_vector(conn)
    return conn


def init_schema_solution(conn: "psycopg2.extensions.connection") -> None:
    """Exercise 3: idempotent DDL for the tickets table (no index yet)."""
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        cur.execute(
            f"""
            CREATE TABLE IF NOT EXISTS tickets (
                id TEXT PRIMARY KEY,
                text TEXT NOT NULL,
                category TEXT,
                severity TEXT,
                embedding vector({db.DIMS}),
                embedded_with TEXT NOT NULL
            );
            """
        )


def check_drift_solution(conn: "psycopg2.extensions.connection") -> list[str]:
    """Exercise 7 (support): model names in the table that differ from the
    configured embedding model."""
    with conn.cursor() as cur:
        cur.execute("SELECT DISTINCT embedded_with FROM tickets;")
        rows = cur.fetchall()
    return sorted({row[0] for row in rows if row[0] != db.EMBEDDING_MODEL})
