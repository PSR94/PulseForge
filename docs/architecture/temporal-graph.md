# Temporal knowledge graph

Every relationship includes a validity window.

```text
(source_entity_id, relationship_type, target_entity_id)
valid_from
valid_to | null
source_count
confidence
strength
evidence_ids[]
```

A snapshot at time `t` includes relationships satisfying:

`valid_from <= t AND (valid_to IS NULL OR valid_to > t)`

Temporal Graph Diff computes additions, removals and strength changes between two snapshots, then
adds state-derived context such as contradictions introduced during the interval, accelerating entities
and emerging topics.

Observational edges such as `CO_OCCURS_WITH` are deliberately named so users cannot mistake a
co-mention for a business or causal relationship.
