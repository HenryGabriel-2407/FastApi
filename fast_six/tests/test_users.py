from http import HTTPStatus

from fast_six.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users/', json={'username': 'testusername', 'email': 'testemail@example.com', 'password': 'testpassword'}
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'username': 'testusername', 'email': 'testemail@example.com', 'id': 1}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/?limit=10&offset=0')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        json={'username': user.username, 'email': user.email, 'password': user.clean_password},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK


def test_get_user(client, user):
    response = client.get(f'/users/{user.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': user.id, 'username': user.username, 'email': user.email}


def test_update_user_unauthorized(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        json={'username': 'bob', 'email': 'bob@example.com', 'password': 'mynewpassword'},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_unauthorized(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_update_integrity_error(client, user, other_user, token):
    response_update = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': other_user.username,
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {'detail': 'Username or Email already exists'}
