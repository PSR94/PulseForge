# AI analyst architecture

The analyst operates over structured intelligence rather than an unbounded document prompt.

```mermaid
sequenceDiagram
    participant U as User
    participant A as Analyst
    participant T as Tool registry
    participant S as Structured state
    participant M as AI provider

    U->>A: Why is NVIDIA appearing more frequently?
    A->>T: calculate_velocity(entity=NVIDIA)
    T->>S: query event appearances / baseline
    S-->>T: 5.7× + deterministic inputs
    A->>T: find_related_events(entity=NVIDIA)
    T->>S: normalized clusters
    S-->>T: events + evidence ids
    A->>M: Explain structured results
    M-->>A: inference
    A-->>U: explanation + citations + uncertainty
```

Provider adapters:
- deterministic mock
- OpenAI Responses structured output
- Azure OpenAI structured chat completion
- local OpenAI-compatible endpoints

Business logic does not depend on a single provider.
