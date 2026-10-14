import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from fastapi.testclient import TestClient
from app import app, activities

client = TestClient(app)


def test_get_activities():
    # Arrange
    # (no setup needed)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "Chess Club" in response.json()


def test_signup_for_activity():
    # Arrange
    email = "newstudent@mergington.edu"
    activity_name = "Chess Club"
    if email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(email)

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]


def test_signup_duplicate_fails():
    # Arrange
    email = "duplicate@mergington.edu"
    activity_name = "Chess Club"
    if email not in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].append(email)

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400


def test_signup_unknown_activity():
    # Arrange
    email = "someone@mergington.edu"

    # Act
    response = client.post("/activities/Nonexistent Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 404