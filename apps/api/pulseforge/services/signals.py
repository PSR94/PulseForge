from __future__ import annotations

from statistics import mean, pstdev


def calculate_velocity(current_mentions: list[int], baseline_mentions: list[int]) -> dict[str, float]:
    if not current_mentions or not baseline_mentions:
        raise ValueError("current and baseline mention windows must be non-empty")
    current_rate = mean(current_mentions)
    baseline_rate = mean(baseline_mentions)
    ratio = current_rate / max(baseline_rate, 0.01)
    return {
        "current_rate": round(current_rate, 2),
        "baseline_rate": round(baseline_rate, 2),
        "velocity_ratio": round(ratio, 2),
        "percent_change": round((ratio - 1) * 100, 1),
    }


def anomaly_z_score(current: float, historical: list[float]) -> float:
    if len(historical) < 2:
        return 0.0
    sigma = pstdev(historical)
    if sigma == 0:
        return 0.0 if current == mean(historical) else 10.0
    return round((current - mean(historical)) / sigma, 2)
