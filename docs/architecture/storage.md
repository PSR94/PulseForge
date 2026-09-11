# Storage strategy

PulseForge's first durable target is PostgreSQL with pgvector. The SQLAlchemy schema in `apps/api/pulseforge/persistence/schema.py` mirrors workspace-isolated sources, documents, entities, events, claims, temporal relationships, and signals. Every high-cardinality table includes `workspace_id` so production authorization can enforce tenant boundaries close to storage.

Vector search belongs in PostgreSQL initially. A production migration should enable `CREATE EXTENSION IF NOT EXISTS vector` and add embedding columns/indexes only for the workloads that use them. OpenSearch and Neo4j are deployment options, not mandatory architecture decorations.

The demo repository intentionally remains deterministic and in-memory so a clone is useful without infrastructure. Production adapters should implement the same domain operations and transactionally persist stage transitions and failures.
