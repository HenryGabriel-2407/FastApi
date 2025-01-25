from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from fast_five.database import get_session
from fast_five.models import User
from fast_five.schemas import UserList, UserPublic, UserSchema
from fast_five.security import get_current_user, get_password_hash

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
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


@router.get('/', response_model=UserList, status_code=HTTPStatus.OK)
def read_users(session=Depends(get_session), limit: int = 10, offset: int = 10):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}


@router.put('/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session=Depends(get_session), current_user=Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions')
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


@router.delete('/{user_id}', status_code=HTTPStatus.OK)
def delete_user(user_id: int, session=Depends(get_session), current_user=Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions')
    session.delete(current_user)
    session.commit()
    return {'message': 'User deleted'}


@router.get('/{user_id}', response_model=UserPublic, status_code=HTTPStatus.OK)
def get_user(user_id: int, session=Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Usuário não existe')
    return db_user
