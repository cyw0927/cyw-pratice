def test_task_response_never_exposes_test_cases(client):
    response = client.get("/api/v1/learning/tasks/1")
    assert response.status_code == 200
    assert "test_cases" not in response.json()


def test_concept_task_list(client):
    response = client.get("/api/v1/learning/concepts/1/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert "test_cases" not in response.json()[0]
