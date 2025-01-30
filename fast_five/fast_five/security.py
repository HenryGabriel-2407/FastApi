from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from jwt.exceptions import ExpiredSignatureError, PyJWTError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_five.database import get_session
from fast_five.models import User
from fast_five.settings import Settings

pwd_content = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

settings = Settings()

T_Session = Annotated[Session, Depends(get_session)]


def get_password_hash(password: str):
    return pwd_content.hash(password)


def verifry_password_hash(plain_password: str, hashed_password: str):
    return pwd_content.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_current_user(session: T_Session, token: str = Depends(oauth2_scheme)):
    credencial_excepctions = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get('sub')
        if not username:
            raise credencial_excepctions
    except ExpiredSignatureError:
        raise credencial_excepctions
    except PyJWTError:
        raise credencial_excepctions
    user = session.scalar(select(User).where(User.email == username))
    if user is None:
        raise credencial_excepctions
    return user
