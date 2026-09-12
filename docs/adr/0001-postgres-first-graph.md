# ADR 0001 — PostgreSQL-first temporal graph

**Status:** Accepted

PulseForge stores temporal relationships in PostgreSQL rather than adding Neo4j solely for appearance.
The first product slice needs transactional evidence/claim/event/relationship updates and temporal
snapshot queries more than deep multi-hop graph traversal. A Neo4j adapter remains possible when
workloads justify independent graph infrastructure.
