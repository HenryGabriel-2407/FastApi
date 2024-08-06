from fastapi import FastAPI
from http import HTTPStatus
from fast_one.schemas import UserSchema, Message, UserPublic
# from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def route():
    return {'message': 'Batatinha voadora atingiu uma torre'}

@app.post('/users/', response_model=UserPublic)
def create_user(user: UserSchema):
    return user
