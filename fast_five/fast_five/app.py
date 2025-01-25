from http import HTTPStatus

from fastapi import FastAPI

from fast_five.routers import auth, users
from fast_five.schemas import Message

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)


@app.get('/', response_model=Message, status_code=HTTPStatus.OK)
def root():
    return {'message': 'Hello, World!', 'batata': 24}
