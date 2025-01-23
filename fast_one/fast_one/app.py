from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_one.schemas import Message

app = FastAPI()


@app.get('/', response_model=Message, status_code=HTTPStatus.OK)
def root():
    return {'message': 'Hello, World!', 'batata': 12}


@app.get('/batatinha', response_class=HTMLResponse)
def batatinha():
    return """
<html>
      <head>
        <title> Nosso olá mundo!</title>
      </head>
      <body>
        <h1> Olá Mundo </h1>
      </body>
    </html>
"""


# task run --host 0.0.0.0
