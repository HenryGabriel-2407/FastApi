from http import HTTPStatus

from fastapi import FastAPI

from fast_one.schemas import Message, UserDb, UserPublic, UserSchema

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
