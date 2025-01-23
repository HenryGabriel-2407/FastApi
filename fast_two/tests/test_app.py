from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from fast_two.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_get(client):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hello, World!", "batata": 24}


def test_create_user(client):
    response = client.post(
        "/users/", json={"username": "testusername", "email": "testemail@example.com", "password": "testpassword"}
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"username": "testusername", "email": "testemail@example.com", "id": 1}


def test_read_users(client):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [{"username": "testusername", "email": "testemail@example.com", "id": 1}]}


def test_update_user(client):
    response = client.put(
        "/users/1", json={"username": "testusername2", "email": "testemail2@example.com", "password": "testpassword2"}
    )
    assert response.json() == {"username": "testusername2", "email": "testemail2@example.com", "id": 1}


def test_get_user(client):
    response = client.get("/users/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"username": "testusername2", "email": "testemail2@example.com", "id": 1}


def test_update_user_not_found(client):
    response = client.put(
        "/users/2", json={"username": "testusername2", "email": "testemail2@example.com", "password": "testpassword2"}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client):
    response = client.delete("/users/1")
    assert response.json() == {"message": "User deleted"}


def test_delete_user_not_found(client):
    response = client.delete("/users/2")
    assert response.status_code == HTTPStatus.NOT_FOUND
