from src.app import activities


def test_get_activities_returns_all_activities(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert activity_name in payload
    assert "description" in payload[activity_name]
    assert "participants" in payload[activity_name]


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    new_email = "new_student@mergington.edu"
    original_participants = activities[activity_name]["participants"].copy()

    try:
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email},
        )

        # Assert
        assert response.status_code == 200
        assert response.json() == {"message": f"Signed up {new_email} for {activity_name}"}
        assert new_email in activities[activity_name]["participants"]
    finally:
        activities[activity_name]["participants"] = original_participants


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = activities[activity_name]["participants"][0]
    original_participants = activities[activity_name]["participants"].copy()

    try:
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email},
        )

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up for this activity"
        assert activities[activity_name]["participants"] == original_participants
    finally:
        activities[activity_name]["participants"] = original_participants


def test_unregister_participant_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    original_participants = activities[activity_name]["participants"].copy()
    email_to_remove = original_participants[0]

    try:
        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email_to_remove},
        )

        # Assert
        assert response.status_code == 200
        assert response.json() == {"message": f"Removed {email_to_remove} from {activity_name}"}
        assert email_to_remove not in activities[activity_name]["participants"]
    finally:
        activities[activity_name]["participants"] = original_participants


def test_unregister_nonexistent_participant_returns_message(client):
    # Arrange
    activity_name = "Chess Club"
    missing_email = "missing_student@mergington.edu"
    original_participants = activities[activity_name]["participants"].copy()

    try:
        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": missing_email},
        )

        # Assert
        assert response.status_code == 200
        assert response.json() == {"message": f"{missing_email} is not registered for {activity_name}"}
        assert activities[activity_name]["participants"] == original_participants
    finally:
        activities[activity_name]["participants"] = original_participants


def test_unregister_invalid_activity_returns_404(client):
    # Arrange
    invalid_activity = "Nonexistent Club"

    # Act
    response = client.post(
        f"/activities/{invalid_activity}/unregister",
        params={"email": "student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
