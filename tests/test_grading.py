def test_submission_is_stored_as_pending(client):
    response = client.post(
        "/api/v1/grading/attempts",
        json={
            "user_id": 1,
            "task_id": 1,
            "context_type": "LEARNING",
            "submitted_code": "def add(a, b): return a + b",
        },
    )
    assert response.status_code == 202
    assert response.json()["status"] == "PENDING"
    assert response.json()["is_correct"] is None
    attempt_id = response.json()["id"]
    assert (
        client.get(f"/api/v1/grading/attempts/{attempt_id}", params={"user_id": 1}).status_code
        == 200
    )


def test_context_ids_are_validated(client):
    response = client.post(
        "/api/v1/grading/attempts",
        json={"user_id": 1, "task_id": 1, "context_type": "DAILY", "submitted_code": "pass"},
    )
    assert response.status_code == 422
