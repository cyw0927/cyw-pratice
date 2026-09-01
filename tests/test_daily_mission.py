from app.db.models import AttendanceTask


def test_duplicate_check_in_is_rejected(client):
    assert client.post("/api/v1/daily-missions/check-in", json={"user_id": 1}).status_code == 201
    assert client.post("/api/v1/daily-missions/check-in", json={"user_id": 1}).status_code == 409


def test_today_mission_and_complete_flow(client, db):
    attendance_id = client.post("/api/v1/daily-missions/check-in", json={"user_id": 1}).json()["id"]
    item = AttendanceTask(attendance_id=attendance_id, task_id=1, task_order=1)
    db.add(item)
    db.commit()
    response = client.get("/api/v1/daily-missions/today", params={"user_id": 1})
    assert response.status_code == 200
    assert response.json()["tasks"][0]["is_completed"] is False
    completed = client.patch(
        f"/api/v1/daily-missions/tasks/{item.id}/complete", params={"user_id": 1}
    )
    assert completed.json()["is_completed"] is True
