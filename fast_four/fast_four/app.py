from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from fast_four.database import get_session
from fast_four.models import User
from fast_four.schemas import Message, Token, UserList, UserPublic, UserSchema
from fast_four.security import create_access_token, get_password_hash, verifry_password_hash, get_current_user

app = FastAPI()


@app.get('/', response_model=Message, status_code=HTTPStatus.OK)
def root():
    return {'message': 'Hello, World!', 'batata': 24}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(select(User).where((User.email == user.email) | (User.username == user.username)))

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Username already exists')
        elif db_user.email == user.email:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Email already exists')

    db_user = User(username=user.username, email=user.email, password=get_password_hash(user.password))
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', response_model=UserList, status_code=HTTPStatus.OK)
def read_users(session=Depends(get_session), limit: int = 10, offset: int = 10):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session=Depends(get_session),  current_user=Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
    try:
        current_user.username = user.username
        current_user.password = get_password_hash(user.password)
        current_user.email = user.email
        session.commit()
        session.refresh(current_user)

        return current_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )


@app.delete('/users/{user_id}', status_code=HTTPStatus.OK)
def delete_user(user_id: int, session=Depends(get_session),  current_user=Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions')
    session.delete(current_user)
    session.commit()
    return {'message': 'User deleted'}


@app.get('/users/{user_id}', response_model=UserPublic, status_code=HTTPStatus.OK)
def get_user(user_id: int, session=Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Usuário não existe')
    return db_user


@app.post('/token', response_model=Token, response_model_exclude_unset=True)
def login_for_access_token(data_form: OAuth2PasswordRequestForm = Depends(), session=Depends(get_session)):
    user = session.scalar(select(User).where(User.email == data_form.username))
    if not user or not verifry_password_hash(data_form.password, user.password):
        raise HTTPException(status_code=400, detail='Incorrect email or password')
    access_token = create_access_token(data={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'Bearer'}
