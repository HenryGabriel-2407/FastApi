from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select

from fast_three.database import get_session
from fast_three.models import User
from fast_three.schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI()


@app.get("/", response_model=Message, status_code=HTTPStatus.OK)
def root():
    return {"message": "Hello, World!", "batata": 24}


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(select(User).where((User.email == user.email) | (User.username == user.username)))

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Username already exists")
        elif db_user.email == user.email:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Email already exists")

    db_user = User(username=user.username, email=user.email, password=user.password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get("/users/", response_model=UserList, status_code=HTTPStatus.OK)
def read_users(session=Depends(get_session), limit: int = 10, offset: int = 10):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {"users": users}


@app.put("/users/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não existe")
    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password
    session.commit()
    session.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}", status_code=HTTPStatus.OK)
def delete_user(user_id: int, session=Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não existe")
    session.delete(db_user)
    session.commit()
    return {"message": "User deleted"}


@app.get("/users/{user_id}", response_model=UserPublic, status_code=HTTPStatus.OK)
def get_user(user_id: int, session=Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não existe")
    return db_user
