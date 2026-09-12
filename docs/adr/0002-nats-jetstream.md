# ADR 0002 — NATS JetStream for local-first streaming

**Status:** Accepted

NATS JetStream provides durable work delivery and replay while remaining lightweight enough for
`docker compose up`. Pipeline messages are stage-oriented and consumers are expected to be idempotent.
Kafka/Redpanda can be introduced behind the event-bus boundary for deployments that already operate it.
