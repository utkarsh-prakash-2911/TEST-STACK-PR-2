import pytest
from fastapi.testclient import TestClient

from stackpr.api import create_app, get_service
from stackpr.service import UserService


@pytest.fixture
def client():
    app = create_app()
    # Use a fresh service per test so state does not leak between tests.
    service = UserService()
    app.dependency_overrides[get_service] = lambda: service
    return TestClient(app)


def test_create_user(client):
    resp = client.post(
        "/users", json={"email": "alice@example.com", "name": "Alice"}
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["email"] == "alice@example.com"
    assert body["role"] == "member"
    assert body["is_active"] is True


def test_get_user_roundtrip(client):
    created = client.post(
        "/users", json={"email": "bob@example.com", "name": "Bob"}
    ).json()

    resp = client.get(f"/users/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == created["id"]


def test_duplicate_email_conflict(client):
    client.post("/users", json={"email": "dup@example.com", "name": "First"})
    resp = client.post(
        "/users", json={"email": "dup@example.com", "name": "Second"}
    )
    assert resp.status_code == 409


def test_get_missing_user_404(client):
    resp = client.get("/users/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404


def test_invalid_email_rejected(client):
    resp = client.post(
        "/users", json={"email": "not-an-email", "name": "Nobody"}
    )
    assert resp.status_code == 422
