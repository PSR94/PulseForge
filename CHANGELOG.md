# Changelog

All notable changes to PulseForge are documented here.

## Unreleased

### Added
- Modular RSS, JSON, web-page, GitHub release, arXiv and Hacker News connectors.
- Deterministic live ingestion materializer that updates events, evidence, entities, observational graph edges and velocity signals.
- Decomposed FastAPI route modules.
- SQLAlchemy persistence expansion plus Alembic migration scaffold.
- Workspace role/JWT primitives and request rate limiting.
- OpenAI, Azure OpenAI, local OpenAI-compatible and deterministic mock AI provider adapters.
- Prometheus metrics and OpenTelemetry tracing integration.
- Watchlist rules, deterministic evaluation and explainable alerts.
- Markdown, HTML and PDF briefing export.
- API-backed Next.js event/evidence/entity/graph/diff/signal/source/watchlist/briefing screens.
- Unified command-palette search.
- Architecture, processing, evidence, graph, AI, security, deployment and observability documentation.
- ADRs for graph storage, streaming and evidence-first AI boundaries.
- CI, CodeQL and real-app screenshot workflows.

### Changed
- PulseForge version advanced to 0.2.0.
- The live source ingestion endpoint now advances through materialization to `INDEXED` in local/demo mode.
- README rebuilt around the real product architecture and end-to-end workflow.
