from http import HTTPStatus

from fast_six.models import TodoState
from tests.conftest import TodoFactory


def test_create_todo(client, token):
    response = client.post(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Test todo', 'description': 'Test todo description', 'state': 'draft'},
    )

    assert response.json() == {'id': 1, 'title': 'Test todo', 'description': 'Test todo description', 'state': 'draft'}


def test_list_todo_should_return_5_todos(session, client, user, token):
    excepted_todos = 5
    session.bulk_save_objects(TodoFactory.create_batch(excepted_todos, user_id=user.id))
    session.commit()
    response = client.get('/todos/', headers={'Authorization': f'Bearer {token}'})

    assert len(response.json()['todos']) == excepted_todos


def test_list_todos_pagination_should_return_2_todos(session, client, user, token):
    excepted_todos = 2
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()
    response = client.get('/todos/?offset=1&limit=2', headers={'Authorization': f'Bearer {token}'})

    assert len(response.json()['todos']) == excepted_todos


def test_list_todo_filter_title_should_return_5_todos(session, client, user, token):
    excepted_todos = 5
    session.bulk_save_objects(TodoFactory.create_batch(excepted_todos, user_id=user.id, title='Todo test 1'))
    session.commit()
    response = client.get('/todos/?title=Todo test 1', headers={'Authorization': f'Bearer {token}'})

    assert len(response.json()['todos']) == excepted_todos


def test_list_todo_filter_description_should_return_5_todos(session, client, user, token):
    excepted_todos = 5
    session.bulk_save_objects(TodoFactory.create_batch(excepted_todos, user_id=user.id, description='Todo test 1'))
    session.commit()
    response = client.get('/todos/?description=Tod', headers={'Authorization': f'Bearer {token}'})

    assert len(response.json()['todos']) == excepted_todos


def test_list_todo_filter_state_should_return_5_todos(session, client, user, token):
    excepted_todos = 5
    session.bulk_save_objects(TodoFactory.create_batch(excepted_todos, user_id=user.id, state=TodoState.doing))
    session.commit()
    response = client.get('/todos/?state=doing', headers={'Authorization': f'Bearer {token}'})

    assert len(response.json()['todos']) == excepted_todos


def test_delete_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()

    response = client.delete(f'/todos/{todo.id}', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Task has been deleted successfully'}


def test_delete_todo_not_found(session, client, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()

    response = client.delete('/todos/10', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}


def test_patch_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()

    response = client.patch(f'/todos/{todo.id}', headers={'Authorization': f'Bearer {token}'}, json={'title': 'Test 1'})

    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'Test 1'


def test_patch_todo_error(client, token):
    response = client.patch('/todos/10', headers={'Authorization': f'Bearer {token}'}, json={})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}
