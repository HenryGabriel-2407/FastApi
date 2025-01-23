from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_two.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get("/", response_model=Message, status_code=HTTPStatus.OK)
def root():
    return {"message": "Hello, World!", "batata": 24}


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(id=len(database) + 1, **user.model_dump())
    database.append(user_with_id)
    return UserPublic(id=user_with_id.id, username=user_with_id.username, email=user_with_id.email)


@app.get("/users/", response_model=UserList, status_code=HTTPStatus.OK)
def read_users():
    return {"users": database}


@app.put("/users/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    user_with_id = UserDB(id=user_id, **user.model_dump())
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete("/users/{user_id}", status_code=HTTPStatus.OK)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    del database[user_id - 1]
    return {"message": "User deleted"}


@app.get("/users/{user_id}", response_model=UserPublic, status_code=HTTPStatus.OK)
def get_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return database[user_id - 1]


"""
1. Escrever um teste para o erro de  404  (NOT FOUND) para o endpoint de PUT ---- Finalizado;
2. Escrever um teste para o erro de  404  (NOT FOUND) para o endpoint de DELETE --- Finalizado;
3. Crie um endpoint GET para pegar um único recurso como  users/{id}  e faça seus testes. ---- Finalizado"""
