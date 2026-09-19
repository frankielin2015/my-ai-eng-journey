# Week 5 — pgvector RAG over Support Tickets

## What this is

A small retrieval-augmented generation (RAG) ingestion and query pipeline over
12 customer support tickets. Tickets are embedded with a local Ollama model
(`nomic-embed-text`, 768 dims), stored in Postgres with the `pgvector`
extension, and retrieved with a distance query using cosine distance.

The scaffold is **exercise-driven**: most function bodies raise
`NotImplementedError` and carry an `Exercise N` docstring with a
Concept / Write / Verify triplet. Work them roughly in order — each one is
slightly harder than the last — then cross-check against `solutions/`.
`db.py` is the single source of truth for the shared constants
(`EMBEDDING_MODEL`, `DIMS`); never re-declare them elsewhere.

## Prerequisites

- Local Ollama with the embedding model pulled:

  ```sh
  ollama pull nomic-embed-text
  ```

- Postgres + pgvector running and **healthy** (the compose service now has a
  `pg_isready` healthcheck, so `--wait` blocks until it actually accepts
  connections):

  ```sh
  docker compose up -d --wait
  ```

- Python deps (both DB packages are declared in `pyproject.toml`):

  ```sh
  uv add psycopg2-binary pgvector
  ```

## How to run end-to-end

```sh
docker compose up -d --wait
uv add psycopg2-binary pgvector
uv run python src/week5/ingest.py
uv run python src/week5/query.py "package not arrived"
```

Once every exercise is implemented, ingest prints `connection ok`, then
`embedding 12 tickets`, then `write ok`; the query prints the model, the
operator, and the top-k tickets ranked by similarity.

## Exercise map

1. **Envelope, paper** — trace one RAG request end to end (collect → embed →
   store → retrieve) on paper before writing code.
2. **Connection adapter** — understand why binding a Python list to a `vector`
   column needs `register_vector(conn)`, and confirm every connection in
   `db.get_connection()` is adapted.
3. **Schema** — implement `init_schema(conn)` in `db.py`: the vector extension
   plus the `tickets` table (no index yet).
4. **Ingest** — implement `embed_tickets` (batched + pairing asserts),
   `upsert_tickets` (idempotent `ON CONFLICT`), and study the single-connection
   `main` flow in `ingest.py`.
5. **Operator** — parameterize pgvector's distance operator (`<=>`, `<->`,
   `<#>`) behind one assert-checked query in `query.py`.
6. **Ranking** — get `ORDER BY` direction and the distance→similarity
   conversion right for each operator, including the `<#>` sign trap.
7. **Drift** — implement `check_drift_warn` on top of `db.check_drift` so a
   model swap is caught before results are trusted.
8. **Chunking** — implement `chunk_fixed`, `chunk_sentences`, and
   `chunk_recursive` in `chunking.py`.
9. **Chunking bake-off** — run all three splitters over `policy.md`, compare
   chunk counts and boundary quality, and pick a default.
10. **Index bake-off** — add the HNSW index to `init_schema` and compare it
    against IVFFlat on build time, query latency, and recall.

## Reference solutions

`solutions/` holds full working implementations for exercises 3–8, openly
committed so you can diff your attempt against them. Every solution function is
suffixed `_solution` (e.g. `from week5.solutions.query_solution import
search_solution`) and its docstring cites the exercise number it answers.
Attempt each exercise first; peeking is fine *after* a self-attempt, but the
learning is in failing the asserts yourself.

## HNSW vs IVFFlat

**HNSW** is a multi-layer navigable small-world graph (not a skip list). Each
layer is a proximity graph; search enters at the top sparse layer and greedily
descends, hopping to nearer neighbours until it reaches the dense bottom layer.
Builds are incremental and the index handles inserts without retraining.
**IVFFlat** clusters vectors with k-means at build time and requires trained
data: it partitions vectors into `lists` cells and at query time scans only the
`probes` nearest cells.

The trade-off: HNSW gives higher recall at low latency and tolerates inserts,
but costs more memory and build time. IVFFlat builds faster and uses less
memory, but its recall is capped by the list/probe configuration and it must be
rebuilt as the data distribution shifts. Start with HNSW for a small,
write-heavy corpus; consider IVFFlat when the corpus is huge and build
time/memory dominate.

## Future work

- Switch from per-ticket rows to actually ingesting chunked documents
  (`chunking.py` is the start; wire it into `ingest.py` next).
- Add contextual retrieval (prepend an LLM-generated 1-line context per chunk)
  — measured ~35% recall improvement in the reference experiments.
- Compare HNSW against IVFFlat at scale (>10K docs) instead of only on paper.
- Add BM25 hybrid search + RRF reranking for queries with exact identifiers
  (order IDs, error codes).
- Persist the embedding model name in the schema and log it on every query
  (the drift check is the first step) to catch model swaps early.

## Source notes

- pgvector README: https://github.com/pgvector/pgvector
- Uses local Ollama embeddings because Ollama Cloud has no `/v1/embeddings`
  endpoint.
