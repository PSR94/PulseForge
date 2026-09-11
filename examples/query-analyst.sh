#!/usr/bin/env sh
curl -sS http://localhost:8000/api/v1/analyst/ask \
  -H 'content-type: application/json' \
  -d '{"question":"Why is NVIDIA appearing more frequently today?"}'
