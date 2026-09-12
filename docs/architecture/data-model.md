# Data model

```mermaid
erDiagram
    WORKSPACE ||--o{ SOURCE : contains
    WORKSPACE ||--o{ ENTITY : tracks
    WORKSPACE ||--o{ EVENT : normalizes
    SOURCE ||--o{ DOCUMENT : produces
    DOCUMENT ||--o{ CLAIM : evidences
    ENTITY ||--o{ CLAIM : subject
    EVENT }o--o{ ENTITY : involves
    EVENT }o--o{ CLAIM : groups
    ENTITY ||--o{ TEMPORAL_RELATIONSHIP : source
    ENTITY ||--o{ TEMPORAL_RELATIONSHIP : target
    WORKSPACE ||--o{ SIGNAL : detects
    WORKSPACE ||--o{ WATCHLIST_RULE : monitors
    WATCHLIST_RULE ||--o{ ALERT : fires
```

PostgreSQL is the canonical durable store. pgvector is the scale-up path for semantic search and event
candidate retrieval; exact/deterministic filters remain ordinary SQL so graph and signal decisions can
be inspected.
