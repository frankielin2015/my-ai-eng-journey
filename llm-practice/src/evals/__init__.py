"""Week 6 — Evals package.

This week measures HOW WELL an LLM task performs. Week 5 gave us retrieval
(pgvector + chunking + RAG); Week 6 asks: how do we know if it works?

The chosen task: extract `{action, owner, due_date}` from a short meeting notes
snippet. The methodology generalizes to any extraction / classification /
generation task — Week 7+ will use the same scaffolding pattern.
"""