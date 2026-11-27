def test_get_activities_returns_activity_data(client):
    # Arrange
    expected_participant = "michael@mergington.edu"

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    assert response.status_code == 200
    assert "Chess Club" in activities
    assert expected_participant in activities["Chess Club"]["participants"]


def test_signup_adds_participant(client):
    # Arrange
    email = "student@mergington.edu"
    activity_path = "/activities/Soccer%20Team/signup"

    # Act
    response = client.post(activity_path, params={"email": email})
    activities = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Soccer Team"}
    assert email in activities["Soccer Team"]["participants"]


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    email = "michael@mergington.edu"
    activity_path = "/activities/Chess%20Club/signup"

    # Act
    response = client.post(activity_path, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_rejects_unknown_activity(client):
    # Arrange
    activity_path = "/activities/Unknown%20Activity/signup"
    email = "student@mergington.edu"

    # Act
    response = client.post(activity_path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_removes_participant(client):
    # Arrange
    email = "michael@mergington.edu"
    activity_path = "/activities/Chess%20Club/signup"

    # Act
    response = client.delete(activity_path, params={"email": email})
    activities = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Chess Club"}
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_rejects_missing_participant(client):
    # Arrange
    activity_path = "/activities/Soccer%20Team/signup"
    email = "student@mergington.edu"

    # Act
    response = client.delete(activity_path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_rejects_unknown_activity(client):
    # Arrange
    activity_path = "/activities/Unknown%20Activity/signup"
    email = "student@mergington.edu"

    # Act
    response = client.delete(activity_path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
