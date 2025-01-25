from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_five.app import app
from fast_five.database import get_session
from fast_five.models import User, table_registry


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        session.commit()

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    user = User(username='Teste', email='teste@test.com', password='testtest')
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def test_get(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello, World!', 'batata': 24}


def test_create_user(client):
    response = client.post(
        '/users/', json={'username': 'testusername', 'email': 'testemail@example.com', 'password': 'testpassword'}
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'username': 'testusername', 'email': 'testemail@example.com', 'id': 1}


def test_read_users_with_users(client, user):
    # user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': []}


def test_update_user(client):
    response = client.put(
        '/users/1', json={'username': 'testusername2', 'email': 'testemail2@example.com', 'password': 'testpassword2'}
    )
    assert response.json() == {'detail': 'Usuário não existe'}


def test_get_user(client, user):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'email': 'teste@test.com', 'id': 1, 'username': 'Teste'}


def test_update_user_not_found(client):
    ...
    # response = client.put('/users/2', json={'detail': 'Usuário não existe'})
    # assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client):
    response = client.delete('/users/1')
    assert response.json() == {'detail': 'Usuário não existe'}


def test_delete_user_not_found(client):
    response = client.delete('/users/2')
    assert response.status_code == HTTPStatus.NOT_FOUND
