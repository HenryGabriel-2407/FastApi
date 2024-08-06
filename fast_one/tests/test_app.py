from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_one.app import app


def test_retornar_OK_root():
    client = TestClient(app)  # Arreange (organização)

    response = client.get('/')  # Act (ação)

    assert response.status_code == HTTPStatus.OK  # assert (afirmação)
    assert response.json() == {'message': 'Batatas voadora atingiu uma torre'}
