"""Week 5 deliverable: HNSW vs IVFFlat index bake-off.

Exercise 10 lives here. The split between this file and `query.py`:

    query.py:    the user-facing search API (assume an index exists)
    benchmark.py: the A/B test of index strategies

Why a separate file: index drops/recreates are destructive — they happen
during a bake-off, never during a normal search. Keeping them apart
makes it harder to call them by accident.

The bake-off runs three rounds on the same 5 test queries:

    Round 1 — baseline:    no index               (DROP any indexes, then seq scan)
    Round 2 — HNSW:        graph-based ANN index
    Round 3 — IVFFlat:     partition-based ANN index (lists=6 for our 40-row corpus)

For each round we capture:
    - latency: median of 10 timed SELECTs in milliseconds
    - recall@k:  fraction of (round-1 top-k) ids that reappear in round-2/3 top-k
    - index size: pg_relation_size
    - build time: time.perf_counter around CREATE INDEX

At ~40 rows, the planner may ignore BOTH indexes (seq scan is faster for tiny
tables). That outcome IS the finding — index choice matters at scale, not in
toy data — and it's worth seeing with your own EXPLAIN ANALYZE.
"""
from __future__ import annotations

import statistics
import sys
import time
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import psycopg2

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from week5 import db
from week5.query import embed_query

# Five realistic customer questions — mixes of "what" / "how" / "when"
# spanning refund, shipping, returns, and account topics.
TEST_QUERIES: list[str] = [
    "How do I get a refund?",
    "What if my package is late?",
    "How much does shipping cost?",
    "What is the return policy?",
    "Can I cancel my subscription?",
]


def drop_indexes(conn: "psycopg2.extensions.connection") -> None:
    """Exercise 10: drop any pre-existing indexes on tickets.embedding.

    Concept: A bake-off needs a clean baseline. The planner will not bother
             with an HNSW index on 40 rows, but if we leave an old index
             lying around it WILL be considered during planning, which
             would make our round-1 baseline non-baseline.

    Write:   Execute two `DROP INDEX IF EXISTS` statements, one for each
             of the index names we plan to create in this bake-off:
               - hnsw_tickets_embedding_idx
               - ivfflat_tickets_embedding_idx
             Run each in its own `cur.execute(sql)` call. Commit once at
             the end (CREATE/DROP INDEX both need a commit in psycopg2).

    Verify:  After running, `\\d tickets` shows no index on the `embedding`
             column. Queries from this point should show "Seq Scan on tickets".
    """
    with conn.cursor() as cur:
        cur.execute("DROP INDEX IF EXISTS hnsw_tickets_embedding_idx")
        cur.execute("DROP INDEX IF EXISTS ivfflat_tickets_embedding_idx")
    conn.commit()
        


def create_hnsw_index(conn: "psycopg2.extensions.connection") -> float:
    """Exercise 10: CREATE INDEX using HNSW with cosine ops, return build ms.

    Concept: HNSW (Hierarchical Navigable Small World) is a graph-based ANN
             index. At build time it constructs a layered graph where each
             node (a vector) connects to its nearest neighbors. Queries do
             a graph walk — very fast, but the index is large on disk and
             slow to build.

             The OPERATOR CLASS `vector_cosine_ops` declares this index is
             used for cosine-distance queries (`<=>`). Use `vector_l2_ops`
             for `<->` and `vector_ip_ops` for `<#>`. Choosing the wrong
             class silently produces a wrong index that the planner never
             picks — a classic foot-gun.

    Write:   1. Start a perf_counter timer
             2. `CREATE INDEX hnsw_tickets_embedding_idx ON tickets USING
                hnsw (embedding vector_cosine_ops)`
             3. Commit
             4. Return elapsed milliseconds (perf_counter returns seconds)

    Verify:  `\\d tickets` shows the index. `EXPLAIN ANALYZE` of a search
             shows "Index Scan using hnsw_tickets_embedding_idx" instead
             of "Seq Scan on tickets". For 40 rows the planner may still
             choose Seq Scan — that is a finding, not a failure.
    """
    t0 = time.perf_counter()
    sql = """
        CREATE INDEX hnsw_tickets_embedding_idx
        ON tickets USING hnsw (embedding vector_cosine_ops)
    """
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()
    return (time.perf_counter() - t0) * 1000  # seconds → ms


def create_ivfflat_index(conn: "psycopg2.extensions.connection", lists: int = 6) -> float:
    """Exercise 10: CREATE INDEX using IVFFlat with cosine ops + lists param.

    Concept: IVFFlat partitions the vectors into `lists` buckets at build
             time. Queries scan only the buckets closest to the query
             vector (controlled by `probes`, default 1). Tradeoffs vs HNSW:
                build:  fast (just cluster, no graph)
                query:  fast at scale, lossy at small scale (boundary effects)
                memory: small

             The `lists` parameter rule of thumb is `sqrt(rows)`. For our
             40-row corpus, `lists=6` is the textbook choice (sqrt(40)≈6.3).
             Lower lists = faster build, worse recall; higher lists = the
             reverse. Tune by `lists × probes ≥ some_target` and measure.

    Write:   Same shape as create_hnsw_index, but:
                sql = f\"\"\"CREATE INDEX ivfflat_tickets_embedding_idx
                          ON tickets USING ivfflat (embedding vector_cosine_ops)
                          WITH (lists = {lists})\"\"\"
             Note the f-string — `lists` is part of DDL syntax, NOT a
             psycopg2 placeholder, so you cannot use `%s` for it. That is
             a real foot-gun: parameterizing `%s` in DDL raises
             `psycopg2.errors.SyntaxError`.

    Verify:  `\\d tickets` shows `ivfflat_tickets_embedding_idx`. For 40
             rows this index may also be ignored by the planner. Note
             the index size in pg_relation_size vs the HNSW index size.
    """
    t0 = time.perf_counter()
    sql = f"""
    CREATE INDEX ivfflat_tickets_embedding_idx ON tickets USING ivfflat (embedding vector_cosine_ops) WITH (lists = {lists})
    """
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()
    return (time.perf_counter() - t0) * 1000  # seconds → ms    


def bench_topk(
    conn: "psycopg2.extensions.connection",
    query_vector: list[float],
    top_k: int = 3,
) -> tuple[list[str], list[float]]:
    """Exercise 10: run top-k search and return (ids, distances).

    Concept: This is the actual retrieval query, identical to query.py's
             `search()` but parameterized only by the index in play. Whichever
             index exists (or doesn't), psycopg2 + pgvector's planner pick
             the right plan.

    Write:   Build sql = \"\"\"SELECT id, embedding <=> %s::vector AS dist
                          FROM tickets
                          ORDER BY embedding <=> %s::vector
                          LIMIT %s\"\"\" — note the vector is passed twice,
             once in SELECT (for the distance column) and once in ORDER BY
             (so the index, if any, can be used).
             cur.execute(sql, (query_vector, query_vector, top_k))
             fetchall() returns list of (id, dist). Build ids and dists as
             separate lists and return as a tuple.

    Verify:  Output is `len == top_k` for both ids and distances. The ids
             are the same row ids as a non-indexed scan would return
             (modulo ties at low distance values).
    """
    sql = """
        SELECT id, embedding <=> %s::vector AS dist
        FROM tickets
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    """
    with conn.cursor() as cur:
        cur.execute(sql, (query_vector, query_vector, top_k))
        rows = cur.fetchall()
    ids = [row[0] for row in rows]
    dists = [float(row[1]) for row in rows]
    return ids, dists


def time_topk(
    conn: "psycopg2.extensions.connection",
    query_vector: list[float],
    top_k: int = 3,
    n_runs: int = 10,
) -> float:
    """Exercise 10: median latency (ms) for n_runs top-k searches.

    Concept: One run is noisy (GC pause, OS scheduling). Median over N is
             a robust single-number summary. Note: we're timing the full
             Python + psycopg2 roundtrip, not just the SQL plan; for this
             bake-off that's the right unit (it's what users feel).

    Write:   Run `bench_topk(conn, query_vector, top_k)` N times. Time each
             run with `time.perf_counter()` (returns seconds). Convert
             each delta to milliseconds. Return `statistics.median(latencies)`.

    Verify:  Median for the baseline (no index) and either index type
             should be sub-millisecond on this corpus. Larger corpora
             is where the gap shows up.
    """
    latencies_ms: list[float] = []
    for _ in range(n_runs):
        t0 = time.perf_counter()
        bench_topk(conn, query_vector, top_k)
        latencies_ms.append((time.perf_counter() - t0) * 1000)
    return statistics.median(latencies_ms)


def recall_at_k(predicted_ids: list[str], ground_truth_ids: list[str]) -> float:
    """Exercise 10: fraction of ground-truth ids present in predicted ids.

    Concept: recall@k = |predicted ∩ ground_truth| / |ground_truth|
             For a perfect index, recall@k = 1.0. For a wrong index that
             returns the wrong top-k, recall@k ≈ 0.

    Write:   Convert both lists to sets. Return
             `len(predicted_set & ground_truth_set) / len(ground_truth_set)`.
             Edge case: empty ground_truth → return 1.0 (vacuously perfect).

    Verify:  When `predicted_ids == ground_truth_ids`, returns 1.0. When
             they share no ids and ground_truth is non-empty, returns 0.0.
    """
    if not ground_truth_ids:
        return 1.0
    predicted_set = set(predicted_ids)
    truth_set = set(ground_truth_ids)
    return len(predicted_set & truth_set) / len(truth_set)


def bake_off() -> None:
    """Exercise 10: orchestrate the three rounds and print a report.

    Concept: The orchestrator. This is what you'll actually run.

    Write:   1. Open a connection with `db.get_connection()`.
             2. Round 1 — baseline:
                  a. drop_indexes(conn)
                  b. for each query in TEST_QUERIES:
                       - ids_r1, _ = bench_topk(conn, embed_query(query))
                       - latency_r1 = time_topk(conn, embed_query(query))
                  Store per-query ids and latency.
             3. Round 2 — HNSW:
                  a. build_h1 = create_hnsw_index(conn)
                  b. for each query: same as round 1
                  c. Compare: recall_at_k(ids_r2, ids_r1), latency change
             4. Round 3 — IVFFlat:
                  a. drop_indexes(conn) first
                  b. build_t2 = create_ivfflat_index(conn, lists=6)
                  c. for each query: same as round 1
                  d. Compare recall and latency
             5. Print a tidy table: query | round-1 latency | round-2 | round-3
                                   | round-2 recall | round-3 recall

    Verify:  All three rounds run without error. Recall for both indexes is
             exactly 1.0 (because at this size even seq scan and IVFFlat
             partition boundaries still hit the same top-k for our queries).
             Build times print. Index sizes print via pg_relation_size.
    """
    # Pre-compute query embeddings ONCE — they don't depend on the index.
    # Doing this inside the loop would re-call Ollama 5×3 = 15 times instead
    # of 5, polluting the latency measurements (we want query latency, not
    # embedding-model latency).
    query_vectors: list[list[float]] = [embed_query(q) for q in TEST_QUERIES]

    def run_round(round_name: str, label: str) -> tuple[list[dict], float, str | None]:
        """Run one round: bench + time + (if not baseline) capture build ms and index size."""
        results: list[dict] = []
        with db.get_connection() as conn:
            drop_indexes(conn)
            print(f"\n=== {round_name} ===")

            # Build step is per-round (none for baseline)
            build_ms: float = 0.0
            index_size: str | None = None
            if label == "baseline":
                print("(no index — sequential scan)")
            elif label == "hnsw":
                build_ms = create_hnsw_index(conn)
                index_size = _measure_index_size(conn, "hnsw_tickets_embedding_idx")
                print(f"build: {build_ms:.1f} ms | size: {index_size}")
            elif label == "ivfflat":
                build_ms = create_ivfflat_index(conn, lists=6)
                index_size = _measure_index_size(conn, "ivfflat_tickets_embedding_idx")
                print(f"build: {build_ms:.1f} ms | size: {index_size}")

            # Per-query benchmark
            for query, qvec in zip(TEST_QUERIES, query_vectors):
                ids, _ = bench_topk(conn, qvec)
                latency_ms = time_topk(conn, qvec)
                results.append({
                    "query": query,
                    "ids": ids,
                    "latency_ms": latency_ms,
                })
        return results, build_ms, index_size

    # === Three rounds ===
    baseline_runs, _, _ = run_round("Round 1: baseline (no index)", "baseline")
    hnsw_runs, hnsw_build_ms, hnsw_size = run_round("Round 2: HNSW", "hnsw")
    ivfflat_runs, ivfflat_build_ms, ivfflat_size = run_round("Round 3: IVFFlat (lists=6)", "ivfflat")

    # === Recall vs baseline, computed per-query for both indexed rounds ===
    for r in hnsw_runs:
        # find matching baseline ids by query text
        baseline_ids = next(b["ids"] for b in baseline_runs if b["query"] == r["query"])
        r["recall_vs_baseline"] = recall_at_k(r["ids"], baseline_ids)
    for r in ivfflat_runs:
        baseline_ids = next(b["ids"] for b in baseline_runs if b["query"] == r["query"])
        r["recall_vs_baseline"] = recall_at_k(r["ids"], baseline_ids)

    # === Report ===
    lines = []
    lines.append("\n" + "=" * 92)
    lines.append(f"  HNSW build: {hnsw_build_ms:.1f} ms | size: {hnsw_size}")
    lines.append(f"  IVFFlat build (lists=6): {ivfflat_build_ms:.1f} ms | size: {ivfflat_size}")
    lines.append("=" * 92)
    lines.append(f"{'query':<40} {'base ms':>9} {'HNSW':>9} {'HNSW rec':>10} {'IVF ms':>9} {'IVF rec':>9}")
    lines.append("-" * 92)
    for base, h, i in zip(baseline_runs, hnsw_runs, ivfflat_runs):
        lines.append(
            f"{base['query'][:40]:<40} "
            f"{base['latency_ms']:>7.2f}  "
            f"{h['latency_ms']:>7.2f}  "
            f"{h['recall_vs_baseline']:>8.2f}  "
            f"{i['latency_ms']:>7.2f}  "
            f"{i['recall_vs_baseline']:>7.2f}"
        )
    lines.append("=" * 92)
    print("\n".join(lines))


def _measure_index_size(conn, index_name: str) -> str:
    """Human-readable size of an index, e.g. '168 kB'. Used by bake_off."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT pg_size_pretty(pg_relation_size(%s))",
            (index_name,),
        )
        return cur.fetchone()[0]


if __name__ == "__main__":
    bake_off()
