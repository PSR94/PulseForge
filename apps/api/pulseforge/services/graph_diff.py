from __future__ import annotations

from pulseforge.domain.models import GraphDiff, GraphSnapshot, RelationshipStrengthChange


def diff_snapshots(
    before: GraphSnapshot,
    after: GraphSnapshot,
    *,
    introduced_contradiction_ids: list[str] | None = None,
    accelerating_entity_ids: list[str] | None = None,
    declining_entity_ids: list[str] | None = None,
    emerging_topics: list[str] | None = None,
) -> GraphDiff:
    before_entities = set(before.entity_ids)
    after_entities = set(after.entity_ids)
    before_rel = {relationship.id: relationship for relationship in before.relationships}
    after_rel = {relationship.id: relationship for relationship in after.relationships}

    changed: list[RelationshipStrengthChange] = []
    for relationship_id in before_rel.keys() & after_rel.keys():
        old = before_rel[relationship_id]
        new = after_rel[relationship_id]
        if old.strength != new.strength:
            changed.append(
                RelationshipStrengthChange(
                    relationship_id=relationship_id,
                    before=old.strength,
                    after=new.strength,
                    delta=round(new.strength - old.strength, 3),
                )
            )

    added_relationships = [after_rel[key] for key in after_rel.keys() - before_rel.keys()]
    removed_relationships = [before_rel[key] for key in before_rel.keys() - after_rel.keys()]
    added_entities = sorted(after_entities - before_entities)
    removed_entities = sorted(before_entities - after_entities)
    emerging_topics = emerging_topics or []
    summary = (
        f"{len(added_entities)} new entities, {len(added_relationships)} new relationships, "
        f"{len(changed)} relationship strength changes, and {len(emerging_topics)} emerging topics."
    )
    return GraphDiff(
        from_at=before.at,
        to_at=after.at,
        added_entity_ids=added_entities,
        removed_entity_ids=removed_entities,
        added_relationships=added_relationships,
        removed_relationships=removed_relationships,
        changed_relationships=sorted(changed, key=lambda item: abs(item.delta), reverse=True),
        introduced_contradiction_ids=introduced_contradiction_ids or [],
        accelerating_entity_ids=accelerating_entity_ids or [],
        declining_entity_ids=declining_entity_ids or [],
        emerging_topics=emerging_topics,
        summary=summary,
    )
