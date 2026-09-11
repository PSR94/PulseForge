from pulseforge.services.signals import anomaly_z_score, calculate_velocity


def test_velocity_is_deterministic():
    result = calculate_velocity([24, 23, 25, 24, 23, 24], [4, 4, 5, 4, 4, 4])
    assert result["velocity_ratio"] > 5
    assert result["percent_change"] > 400


def test_anomaly_score_handles_flat_history():
    assert anomaly_z_score(8, [2, 2, 2, 2]) == 10.0
