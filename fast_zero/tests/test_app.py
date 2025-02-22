from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def testar_root():
    client = TestClient(app)
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'Message': 'Hello World'}
