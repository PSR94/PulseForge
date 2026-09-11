from fastapi.testclient import TestClient

from pulseforge.main import app

client = TestClient(app)


def test_demo_feed_contains_normalized_events():
    response = client.get("/api/v1/feed")
    assert response.status_code == 200
    body = response.json()
    assert any(item["id"] == "evt-nvidia-platform" and item["source_count"] == 5 for item in body)


def test_conflict_api_keeps_both_claims():
    response = client.get("/api/v1/claims/conflicts")
    assert response.status_code == 200
    conflict = response.json()[0]
    values = {claim["object_value"] for claim in conflict["claims"]}
    assert values == {"October 2026", "January 2027"}


def test_analyst_uses_structured_tools_and_citations():
    response = client.post("/api/v1/analyst/ask", json={"question": "Why is NVIDIA appearing more frequently today?"})
    assert response.status_code == 200
    body = response.json()
    assert "calculate_velocity" in body["tools_used"]
    assert any(item["id"] == "sig-nvidia-velocity" for item in body["citations"])
    assert body["answer_type"] == "inference"


def test_invalid_graph_diff_range_fails():
    response = client.get(
        "/api/v1/graph/diff",
        params={"from": "2026-09-11T12:00:00Z", "to": "2026-09-11T10:00:00Z"},
    )
    assert response.status_code == 422
