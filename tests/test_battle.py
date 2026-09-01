def create_room(client, capacity=2):
    return client.post(
        "/api/v1/battle/rooms",
        json={
            "host_user_id": 1,
            "title": "First room",
            "max_participants": capacity,
            "task_ids": [1],
        },
    )


def test_create_join_capacity_ready_and_hidden_tests(client):
    room_id = create_room(client).json()["id"]
    assert (
        client.post(f"/api/v1/battle/rooms/{room_id}/participants", json={"user_id": 2}).status_code
        == 201
    )
    assert (
        client.post(f"/api/v1/battle/rooms/{room_id}/participants", json={"user_id": 2}).status_code
        == 409
    )
    ready = client.patch(
        f"/api/v1/battle/rooms/{room_id}/ready", json={"user_id": 2, "is_ready": True}
    )
    assert ready.json()["is_ready"] is True
    assert "test_cases" not in client.get(f"/api/v1/battle/rooms/{room_id}/tasks").json()[0]["task"]


def test_full_room_rejects_join(client):
    room_id = create_room(client, 1).json()["id"]
    assert (
        client.post(f"/api/v1/battle/rooms/{room_id}/participants", json={"user_id": 2}).status_code
        == 409
    )
