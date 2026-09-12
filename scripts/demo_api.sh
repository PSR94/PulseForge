#!/usr/bin/env bash
set -euo pipefail
BASE="${PULSEFORGE_API_URL:-http://localhost:8000}"

echo "== Health =="
curl -fsS "$BASE/health" | python -m json.tool

echo "== Signals =="
curl -fsS "$BASE/api/v1/signals" | python -m json.tool

echo "== Temporal Graph Diff =="
curl -fsS "$BASE/api/v1/graph/diff?from=2026-09-10T15%3A40%3A00Z&to=2026-09-11T15%3A40%3A00Z" | python -m json.tool

echo "== Analyst =="
curl -fsS -X POST "$BASE/api/v1/analyst/ask" \
  -H 'content-type: application/json' \
  -d '{"question":"Why is NVIDIA appearing more frequently today?","workspace_id":"ai-industry"}' \
  | python -m json.tool
