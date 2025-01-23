from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from http import HTTPStatus

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fast_four.database import get_session
from fastapi import Depends, HTTPException
from sqlalchemy import select
from fast_four.models import User

from jwt import encode, decode
from jwt.exceptions import PyJWTError
from pwdlib import PasswordHash

SECRET_KEY = 'your-secret-key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_content = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password: str):
    return pwd_content.hash(password)


def verifry_password_hash(plain_password: str, hashed_password: str):
    return pwd_content.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    credencial_excepctions = HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Could not validate credentials", headers={'WWW-Authenticate': 'Bearer'})
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if not username:
            raise credencial_excepctions
    except PyJWTError:
        raise credencial_excepctions
    user = session.scalar(select(User).where(User.email == username))
    if user is None:
        raise credencial_excepctions
    return user