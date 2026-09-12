from __future__ import annotations

from functools import lru_cache

from pulseforge.domain.watchlists import Alert, WatchlistRule


class DemoWatchlistStore:
    def __init__(self) -> None:
        self.rules: list[WatchlistRule] = []
        self.alerts: list[Alert] = []

    def list_rules(self, workspace_id: str) -> list[WatchlistRule]:
        return [rule for rule in self.rules if rule.workspace_id == workspace_id]

    def put_rule(self, rule: WatchlistRule) -> WatchlistRule:
        self.rules = [item for item in self.rules if item.id != rule.id]
        self.rules.append(rule)
        return rule

    def delete_rule(self, rule_id: str) -> bool:
        before = len(self.rules)
        self.rules = [item for item in self.rules if item.id != rule_id]
        return len(self.rules) != before

    def add_alerts(self, alerts: list[Alert]) -> None:
        known = {alert.id for alert in self.alerts}
        self.alerts.extend(alert for alert in alerts if alert.id not in known)

    def list_alerts(self, workspace_id: str) -> list[Alert]:
        return sorted(
            [alert for alert in self.alerts if alert.workspace_id == workspace_id],
            key=lambda alert: alert.fired_at,
            reverse=True,
        )


@lru_cache
def get_watchlist_store() -> DemoWatchlistStore:
    return DemoWatchlistStore()
