# Deployment

Production deployments should switch:

```env
PULSEFORGE_DEMO_MODE=false
PULSEFORGE_REPOSITORY_MODE=database
PULSEFORGE_AUTH_MODE=jwt
PULSEFORGE_JWT_SECRET=<secret-manager-value>
PULSEFORGE_AI_PROVIDER=openai|azure_openai|local
```

Recommended topology:

```mermaid
flowchart TB
    LB[Ingress / TLS] --> WEB[Next.js replicas]
    LB --> API[FastAPI replicas]
    API --> PG[(PostgreSQL + pgvector)]
    API --> REDIS[(Redis)]
    API --> NATS[(NATS JetStream)]
    NATS --> W1[Intelligence workers]
    NATS --> W2[Ingestion workers]
    W1 --> PG
    W2 --> PG
    API --> OTEL[OpenTelemetry Collector]
    W1 --> OTEL
    OTEL --> OBS[Metrics / traces backend]
```

Run Alembic migrations before promoting API/worker replicas. Use managed Postgres backups, NATS stream
replication, a secret manager, outbound egress controls and a reverse proxy that enforces request/body
limits.
