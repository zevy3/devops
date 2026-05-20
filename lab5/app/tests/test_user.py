import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_existed_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"


def test_get_not_existed_user():
    response = client.get("/users/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_create_user():
    payload = {"name": "Charlie", "email": "charlie@example.com"}
    response = client.post("/users/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Charlie"
    assert data["email"] == "charlie@example.com"
    assert "id" in data


def test_create_user_with_invalid_data():
    response = client.post("/users/", json={"name": "NoEmail"})
    assert response.status_code == 422


def test_delete_user():
    create_resp = client.post("/users/", json={"name": "ToDelete", "email": "del@example.com"})
    assert create_resp.status_code == 201
    user_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/users/{user_id}")
    assert delete_resp.status_code == 204

    get_resp = client.get(f"/users/{user_id}")
    assert get_resp.status_code == 404
