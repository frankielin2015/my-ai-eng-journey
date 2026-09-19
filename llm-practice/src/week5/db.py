"""Week 5 deliverable: Postgres + pgvector connection and schema helpers.

Keeps all DB concerns in one place so ingest.py and query.py stay focused on
embeddings and ranking.

Deliberate choice: psycopg2 (v2.x), NOT psycopg3. The v2 API is the simplest
stable one (`psycopg2.connect(...)` + `cursor.execute`), and every pgvector
Python example assumes it. v3 would be fine, but mixing the two APIs in a
small teaching repo adds confusion for no benefit.

This module is the SINGLE SOURCE OF TRUTH for the embedding model name and
vector width. ingest.py, query.py, and chunking.py import them from here so a
model swap only has to happen in one place.

Connection lifecycle (see `get_connection`): the caller owns the connection
and is responsible for `conn.close()`. Do NOT wrap the top-level connection in
a `with conn:` block — psycopg2's connection context manager only manages the
transaction, it does NOT close the socket, so `with get_connection()` leaks
file descriptors on long-running processes.
"""
from __future__ import annotations

try:
    import psycopg2
except ImportError as exc:  # pragma: no cover - import guard
    raise ImportError(
        "psycopg2 is not installed. Install it with:\n"
        "    uv add psycopg2-binary\n"
        "or, without uv:\n"
        "    pip install psycopg2-binary"
    ) from exc

try:
    from pgvector.psycopg2 import register_vector
except ImportError as exc:  # pragma: no cover - import guard
    raise ImportError(
        "pgvector is not installed. Install it with:\n"
        "    uv add pgvector\n"
        "or, without uv:\n"
        "    pip install pgvector"
    ) from exc


CONNECTION_PARAMS = {
    "dbname": "rag",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
}

# Shared constants — import these, never re-declare them elsewhere.
EMBEDDING_MODEL = "nomic-embed-text"
DIMS = 768


def get_connection() -> "psycopg2.extensions.connection":
    """Open a connection to the local rag database (docker compose `db`).

    Registers the pgvector type adapter on EVERY connection, so a plain
    Python list can be passed as a parameter and psycopg2 will serialize it
    for a `vector` column. Without `register_vector`, `%s::vector` with a
    Python list raises `can't adapt type 'list'` — the #1 pgvector gotcha.

    Returns the raw connection. The CALLER owns its lifetime and must call
    `conn.close()` (psycopg2's `with conn:` does not close the socket).
    """
    conn = psycopg2.connect(**CONNECTION_PARAMS)
    register_vector(conn)
    return conn


def init_schema(conn: "psycopg2.extensions.connection") -> None:
    """Exercise 3: init_schema (DDL)
    Concept: Idempotent DDL — `CREATE EXTENSION IF NOT EXISTS` and
             `CREATE TABLE IF NOT EXISTS` let every ingest run re-assert the
             schema without special-casing "already exists".
    Write:   Use the passed-in connection (do NOT open a new one) to run
             `CREATE EXTENSION IF NOT EXISTS vector;` and a
             `CREATE TABLE IF NOT EXISTS tickets` with columns:
                 id            TEXT PRIMARY KEY,
                 text          TEXT NOT NULL,
                 category      TEXT,
                 severity      TEXT,
                 embedding     vector(768),   -- use the DIMS constant
                 embedded_with TEXT NOT NULL
             Do NOT create an index here — that is exercise 10's bake-off.
    Verify:  Re-run ingest twice; the second run must not error. In psql,
             `\\d tickets` shows the six columns and a vector(768) type.
    """
    with conn.cursor() as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS tickets (
        id TEXT PRIMARY KEY, 
        text TEXT NOT NULL, 
        category TEXT, 
        severity TEXT, 
        embedding vector({DIMS}), 
        embedded_with TEXT NOT NULL)
        """)


def check_drift(conn: "psycopg2.extensions.connection") -> list[str]:
    """Returns model names stored in the DB that differ from EMBEDDING_MODEL.

    Drift happens when someone re-ingests with a different embedding model.
    Vectors from two models live in different spaces, so mixing them silently
    corrupts similarity search. Empty list == no drift. Used by query.py's
    `check_drift_warn` (exercise 7).

    Full implementation (not a TODO): a DISTINCT over one text column is the
    cheapest possible check, and callers only read the return value.
    """
    with conn.cursor() as cur:
        cur.execute("SELECT DISTINCT embedded_with FROM tickets;")
        rows = cur.fetchall()
    return sorted({row[0] for row in rows if row[0] != EMBEDDING_MODEL})
