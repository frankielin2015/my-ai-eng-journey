"""Week 5 deliverable: ingest 12 support tickets into Postgres + pgvector.

Pattern (Week 4's index command, moved into Postgres):
    collect: read src/midterm/tickets_corpus.json (one ticket = one row)
    connect: psycopg2 -> rag database, init_schema (idempotent)
    embed:   batch through local Ollama (`nomic-embed-text`)
    store:   UPSERT into tickets(embedding vector(768), embedded_with)
    commit:  once, then close

Connection discipline (fixes the scaffold's bugs):
  - ONE connection is opened in `main` and threaded into every helper. The
    old scaffold opened a second, unused connection; don't reintroduce it.
  - Callers explicitly `conn.close()` in a `finally`. A `with get_connection()`
    block does NOT close the psycopg2 socket.
  - `embed_tickets` does not take a connection at all — it only calls Ollama.

Idempotent: `ON CONFLICT (id) DO UPDATE`, so re-running refreshes each row
instead of duplicating it. `embedded_with` records the model name so a model
swap shows up as drift (see db.check_drift / query.check_drift_warn).

Usage:
    uv run python src/week5/ingest.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import psycopg2

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from client import make_embedder

from week5 import db

CORPUS_PATH = Path(__file__).resolve().parent.parent / "midterm" / "tickets_corpus.json"


def load_corpus() -> list[dict]:
    """Collect: read the ticket corpus as a list of dicts."""
    return json.loads(CORPUS_PATH.read_text(encoding="utf-8"))


def embed_tickets(tickets: list[dict], batch_size: int = 4) -> list[dict]:
    """Exercise 4: embed_tickets (batched embedding)
    Concept: Batch an unbounded corpus through the embeddings API in fixed
             groups, and defend the POSITIONAL pairing between input and
             output — data[i] must belong to tickets[i].
    Write:   Loop over the corpus in slices of `batch_size`; for each slice
             send `input=[ticket["text"] for ticket in batch]` to
             `make_embedder().embeddings.create(model=db.EMBEDDING_MODEL, ...)`,
             then assert (1) `len(response.data) == len(batch)` (truncation
             guard) and (2) `record.index == i` for each position (pairing
             guard) before assigning `batch[i]["embedding"] = record.embedding`.
             Return the same `tickets` list, mutated in place.
    Verify:  len(tickets) rows each have a 768-float "embedding"; temporarily
             slicing with a bad batch_size still pairs correctly, and the two
             asserts fire if the API ever drops or reorders records.
    """
    embedder = make_embedder()
    for i in range(0, len(tickets), batch_size):
        batch = tickets[i : i + batch_size]
        response = embedder.embeddings.create(
            model=db.EMBEDDING_MODEL,
            input=[ticket["text"] for ticket in batch])
        assert len(response.data) == len(batch), f"Got {len(response.data)} vectors for {len(batch)} tickets"
        for j, record in enumerate(response.data):
            assert j == record.index, f"index mismatch: {record.index} != {j}"
            batch[j]["embedding"] = record.embedding
    return tickets


def upsert_tickets(conn: "psycopg2.extensions.connection", tickets: list[dict]) -> None:
    """Exercise 4: upsert_tickets (idempotent write)
    Concept: UPSERT keeps ingest re-runnable — `ON CONFLICT (id) DO UPDATE`
             refreshes the text, metadata, vector, and model stamp instead of
             raising a duplicate-key error.
    Write:   Using the passed-in `conn` (do NOT open another), execute one
             INSERT per ticket into `tickets (id, text, category, severity,
             embedding, embedded_with)` with placeholders `%s`, passing the
             Python list vector as `%s::vector`, and `ON CONFLICT (id) DO
             UPDATE SET` on every non-PK column using `EXCLUDED.*`. Do not
             commit — `main` owns the single commit.
    Verify:  Run ingest twice; `SELECT count(*) FROM tickets` stays 12 and
             `embedded_with` is `nomic-embed-text` on every row.
    """
    with conn.cursor() as cursor:
        sql_statement = """INSERT INTO tickets 
             (id, text, category, severity, embedding, embedded_with) VALUES (%s, %s, %s, %s, %s::vector, %s)
             ON CONFLICT (id) DO UPDATE SET 
             text          = EXCLUDED.text,
             category      = EXCLUDED.category,
             severity      = EXCLUDED.severity,
             embedding     = EXCLUDED.embedding,
             embedded_with = EXCLUDED.embedded_with
             """
        for ticket in tickets:
             ticket_data = (
                 ticket["id"],                             
                 ticket["text"],                           
                 ticket["category"],                        
                 ticket["severity"],                        
                 ticket["embedding"],                       
                 db.EMBEDDING_MODEL)                          
             cursor.execute(sql_statement, ticket_data)
            



def main() -> int:
    """Exercise 4 (partial): the single-connection ingest flow.

    The call order below is intentionally complete and correct: open ONE
    connection, init the schema, embed, upsert, commit once, close in a
    `finally`. Study it, then implement the TODO functions it calls. Do not
    add a second connection and do not wrap the top-level conn in `with`.
    """
    tickets = load_corpus()
    conn = db.get_connection()
    try:
        print("connection ok")
        db.init_schema(conn)
        print(f"embedding {len(tickets)} tickets")
        embed_tickets(tickets)
        upsert_tickets(conn, tickets)
        conn.commit()
        print("write ok")
    except Exception as exc:  # noqa: BLE001 - report and fail with exit 1
        conn.rollback()
        print(f"ingest failed: {exc}", file=sys.stderr)
        return 1
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
