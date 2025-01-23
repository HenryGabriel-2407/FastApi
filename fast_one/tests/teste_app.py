from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_one.app import app


def test_root():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello, World!', 'batata': 12}
