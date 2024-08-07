from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from fast_one.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_retornar_OK_root(client):

    response = client.get('/')  # Act (ação)

    assert response.status_code == HTTPStatus.OK  # assert (afirmação)
    assert response.json() == {'message': 'Batatinha voadora atingiu uma torre'}


def test_create_user(client):
    response = client.post('/users/',  # UserSchema
                json={'nome': 'testusername',
                      'email': 'test@email.com',
                      'senha': 'pass123'})
    # Status code está correto?
    assert response.status_code == HTTPStatus.CREATED
    # Verificar UserPublic
    assert response.json() == {'id': 1,
                                'nome': 'testusername',
                                'email': 'test@email.com'}
