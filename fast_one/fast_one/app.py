from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_one.schemas import Message, UserDb, UserList, UserPublic, UserSchema

# from fastapi.responses import HTMLResponse

app = FastAPI()
database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def route():
    return {'message': 'Batatinha voadora atingiu uma torre'}


@app.post('/users/', response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(user: UserSchema):
    user_with_id = UserDb(id=(len(database) + 1), **user.model_dump())
    # **user.model_dump() vai converter o objeto em dict
    database.append(user_with_id)
    return user_with_id


@app.get('/users/', response_model=UserList)
def read_users():
    return {'users': database}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Not Found')
    user_with_id = UserDb(id=user_id, **user.model_dump())
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Not Found')
    del database[user_id - 1]
    return {'message': 'User deleted'}

'''Escrever um teste para o erro de 404 (NOT FOUND) para o endpoint de PUT;
Escrever um teste para o erro de 404 (NOT FOUND) para o endpoint de DELETE;
Criar um endpoint de GET para pegar um único recurso como users/{id} e fazer seus testes.
Ver: Live sobre SQLAchemy - 258; Live sobre Migrações - 211
'''