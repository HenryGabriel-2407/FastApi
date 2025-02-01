from http import HTTPStatus

from fastapi import FastAPI

from fast_six.schemas import Message
from routers import auth, todo, users

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todo.router)


@app.get('/', response_model=Message, status_code=HTTPStatus.OK)
def root():
    return {'message': 'Hello, World!'}
