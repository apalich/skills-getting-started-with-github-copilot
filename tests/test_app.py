from fastapi.testclient import TestClient
import copy

from src.app import app, activities

client = TestClient(app)

ORIGINAL_ACTIVITIES = copy.deepcopy(activities)


def setup_function():
    # reset activities before each test
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))


def teardown_function():
    # reset activities after each test
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity_name = "Chess Club"
    email = "teststudent@mergington.edu"

    # ensure not present initially
    assert email not in activities[activity_name]["participants"]

    # signup
    resp = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert resp.status_code == 200
    j = resp.json()
    assert "Signed up" in j["message"]

    # now present
    resp = client.get("/activities")
    participants = resp.json()[activity_name]["participants"]
    assert email in participants

    # unregister
    resp = client.delete(f"/activities/{activity_name}/participants?email={email}")
    assert resp.status_code == 200
    j = resp.json()
    assert "Unregistered" in j["message"]

    # ensure removed
    resp = client.get("/activities")
    participants = resp.json()[activity_name]["participants"]
    assert email not in participants
