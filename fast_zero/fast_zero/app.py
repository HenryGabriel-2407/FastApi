#poetry shell
#poetry add fastapi
#poetry update package
#fastapi dev fast_zero/app.py

from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def read_root():
    return 'Batata voadora atingiu uma torre'