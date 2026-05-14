def test_get_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity_success(client):
    activity_name = "Basketball Team"
    email = "newstudent@mergington.edu"

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    response = client.get("/activities")
    activities = response.json()
    assert email in activities[activity_name]["participants"]


def test_signup_activity_not_found(client):
    response = client.post(
        "/activities/Nonexistent Activity/signup",
        params={"email": "test@example.com"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_already_signed_up(client):
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_activity_full(client):
    activity_name = "Chess Club"
    response = client.get("/activities")
    activities = response.json()
    current_count = len(activities[activity_name]["participants"])
    max_participants = activities[activity_name]["max_participants"]

    for i in range(max_participants - current_count):
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": f"filler{i}@mergington.edu"},
        )

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": "overflow@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"


def test_unregister_from_activity_success(client):
    signup_email = "unregister-test@mergington.edu"
    activity_name = "Programming Class"

    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": signup_email},
    )

    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": signup_email},
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {signup_email} from {activity_name}"}

    response = client.get("/activities")
    activities = response.json()
    assert signup_email not in activities[activity_name]["participants"]


def test_unregister_activity_not_found(client):
    response = client.delete(
        "/activities/Nonexistent Activity/unregister",
        params={"email": "test@example.com"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_not_registered(client):
    response = client.delete(
        "/activities/Basketball Team/unregister",
        params={"email": "notregistered@example.com"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not registered for this activity"
