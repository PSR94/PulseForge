import type { Entity, GraphDiff } from "@/lib/types";

function names(ids: string[], entities: Entity[]) {
  const lookup = new Map(entities.map((entity) => [entity.id, entity.name]));
  return ids.map((id) => lookup.get(id) ?? id);
}

export function GraphDiffPanel({ diff, entities }: { diff: GraphDiff; entities: Entity[] }) {
  const added = names(diff.added_entity_ids, entities);
  const accelerating = names(diff.accelerating_entity_ids, entities);
  const declining = names(diff.declining_entity_ids, entities);

  return (
    <section className="card" id="diff">
      <div className="panel-head">
        <h2>Temporal Graph Diff</h2>
        <span>
          {new Date(diff.from_at).toLocaleString()} → {new Date(diff.to_at).toLocaleString()}
        </span>
      </div>
      <div className="diff-grid">
        <div className="diff-col">
          <h3>Added</h3>
          {added.map((item) => (
            <div className="diff-item diff-plus" key={`entity-${item}`}>
              + entity · {item}
            </div>
          ))}
          {diff.added_relationships.map((rel) => (
            <div className="diff-item diff-plus" key={rel.id}>
              + {rel.source_entity_id} <strong>{rel.relationship_type}</strong> {rel.target_entity_id}
            </div>
          ))}
        </div>
        <div className="diff-col">
          <h3>Changed</h3>
          {accelerating.map((item) => (
            <div className="diff-item diff-change" key={`up-${item}`}>
              ↑ accelerating · {item}
            </div>
          ))}
          {declining.map((item) => (
            <div className="diff-item diff-change" key={`down-${item}`}>
              ↓ declining · {item}
            </div>
          ))}
          {diff.changed_relationships.map((change) => (
            <div className="diff-item diff-change" key={change.relationship_id}>
              ~ {change.relationship_id} {change.before.toFixed(2)} → {change.after.toFixed(2)}
            </div>
          ))}
          {diff.emerging_topics.map((topic) => (
            <div className="diff-item diff-change" key={topic}>
              ↑ emerging topic · {topic}
            </div>
          ))}
        </div>
        <div className="diff-col">
          <h3>Removed / uncertainty</h3>
          {diff.removed_relationships.map((rel) => (
            <div className="diff-item" key={rel.id}>
              − {rel.source_entity_id} {rel.relationship_type} {rel.target_entity_id}
            </div>
          ))}
          {diff.introduced_contradiction_ids.map((id) => (
            <div className="diff-item diff-warn" key={id}>
              ⚠ contradiction introduced · {id}
            </div>
          ))}
          {diff.removed_entity_ids.map((id) => (
            <div className="diff-item" key={id}>
              − entity · {id}
            </div>
          ))}
        </div>
      </div>
      <div className="card-sub" style={{ padding: "0 14px 14px" }}>
        {diff.summary}
      </div>
    </section>
  );
}
