from http import HTTPStatus


def test_get(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello, World!', 'batata': 24}
