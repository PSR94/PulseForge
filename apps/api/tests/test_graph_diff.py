from pulseforge.services.demo_repository import dt, get_demo_repository


def test_temporal_diff_exposes_new_relationship_and_contradiction():
    repo = get_demo_repository()
    diff = repo.temporal_diff(dt("2026-09-10T15:00:00Z"), dt("2026-09-11T15:40:00Z"))
    assert "rel-nvidia-nebula" in {relationship.id for relationship in diff.added_relationships}
    assert "con-forge-launch" in diff.introduced_contradiction_ids
    assert "ent-nvidia" in diff.accelerating_entity_ids
