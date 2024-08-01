# poetry shell
# poetry add fastapi
# poetry update package
# fastapi dev fast_zero/app.py

from fastapi import FastAPI
from fast_zero.schemas import Message
# from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get('/', response_model=Message) # response_class = HTMLResponse // por padrão FastApi retorna em json, então é importante especificar
def read_root():
    return {'message': 'Batata voadora atingiu uma torre', 'batata': 100} # em relação ao chemas, se não colocar os dados "requisitados" ou incorretos, vai ocorrer um error 500 (prefiro morrer do perder a vida)
