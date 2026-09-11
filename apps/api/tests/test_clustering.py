from pulseforge.services.clustering import ClusterFeatures, decide_cluster


def test_related_reports_cluster_with_explanation():
    decision = decide_cluster(
        ClusterFeatures(
            shared_entity_ratio=1.0,
            semantic_similarity=0.93,
            topic_similarity=0.9,
            location_match=1.0,
            event_type_match=1.0,
            hours_apart=1.5,
        )
    )
    assert decision.grouped
    assert decision.score >= 0.8
    assert any("semantic" in reason for reason in decision.reasons)


def test_weakly_related_reports_do_not_cluster():
    decision = decide_cluster(
        ClusterFeatures(
            shared_entity_ratio=0,
            semantic_similarity=0.25,
            topic_similarity=0.2,
            location_match=0,
            event_type_match=0,
            hours_apart=48,
        )
    )
    assert not decision.grouped
