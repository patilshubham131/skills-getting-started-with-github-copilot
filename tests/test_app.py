from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_unregister_participant_from_activity():
    activity_name = "Chess Club"
    original_participants = activities[activity_name]["participants"].copy()
    email_to_remove = original_participants[0]

    response = client.post(
        f"/activities/{activity_name}/unregister?email={email_to_remove}"
    )

    assert response.status_code == 200
    assert email_to_remove not in activities[activity_name]["participants"]
    assert activities[activity_name]["participants"] == original_participants[1:]

    # Restore state for the next test run
    activities[activity_name]["participants"] = original_participants
