# Architecture overview

PulseForge is organized around domain boundaries rather than framework boundaries. Connectors produce source documents; normalization and enrichment produce stable inputs; entity resolution and event clustering create structured state; the claim engine attaches evidence; the temporal graph records relationships with validity; signals operate on stored measurements; the analyst queries those layers through explicit tools.

The initial repository uses an in-memory deterministic demo repository so contributors can explore the complete intelligence experience with no infrastructure or API keys. PostgreSQL/pgvector, Redis, and NATS JetStream are included in Compose and intentionally sit behind adapters. This makes the vertical slice real without forcing every contributor to provision external services before they can understand the product.

## Non-negotiable boundary

An LLM may extract or explain, but it does not establish event occurrence, corroboration, graph-diff state, or threshold crossings. Those are domain/service responsibilities with inspectable inputs.
