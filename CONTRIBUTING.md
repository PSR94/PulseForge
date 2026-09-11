# Contributing to PulseForge

Thanks for helping build evidence-first event intelligence.

## Principles

1. Keep facts, claims, evidence, inference, and prediction distinct.
2. Prefer deterministic system state for thresholds, corroboration, clustering rationale, and graph changes.
3. Store provenance for model-assisted extraction decisions.
4. Never silently discard failed ingestion work.
5. Add tests for domain rules before adding UI polish around them.

## Development

```bash
cp .env.example .env
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
cd apps/web && npm install && npm test
```

Use conventional commit-style messages where practical. Pull requests should describe the evidence/provenance implications of changes to ingestion, claims, signals, or analyst output.
