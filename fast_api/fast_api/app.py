from fastapi import FastAPI
app = FastAPI()

app.get('/')
def read_root():
    return {'message':'Batatas voadoras'}

#poetry shell
#fastapi dev fast_api app.py