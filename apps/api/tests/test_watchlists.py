from pulseforge.domain.watchlists import WatchCondition, WatchTargetType, WatchlistRule
from pulseforge.services.demo_repository import get_demo_repository
from pulseforge.services.watchlists import evaluate_rule


def test_velocity_watchlist_fires_with_explanation():
    repo = get_demo_repository()
    rule = WatchlistRule(
        id="watch-test",
        workspace_id=repo.workspace.id,
        name="NVIDIA spike",
        target_type=WatchTargetType.ENTITY,
        target="NVIDIA",
        conditions=[WatchCondition(field="multiplier", operator="gte", value=4)],
    )
    alerts = evaluate_rule(rule, events=repo.events, signals=repo.signals)
    assert alerts
    assert "deterministic threshold" in alerts[0].explanation
    assert float(alerts[0].metrics["multiplier"]) >= 4
