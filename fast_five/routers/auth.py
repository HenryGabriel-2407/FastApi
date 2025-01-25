from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_five.database import get_session
from fast_five.models import User
from fast_five.schemas import Token
from fast_five.security import create_access_token, verifry_password_hash

router = APIRouter(prefix='/auth', tags=['auth'])
T_OAuth2 = Annotated[OAuth2PasswordRequestForm, Depends()]
T_Session = Annotated[Session, Depends(get_session)]


@router.post('/token', response_model=Token, response_model_exclude_unset=True)
def login_for_access_token(data_form: T_OAuth2, session: T_Session):
    user = session.scalar(select(User).where(User.email == data_form.username))
    if not user or not verifry_password_hash(data_form.password, user.password):
        raise HTTPException(status_code=400, detail='Incorrect email or password')
    access_token = create_access_token(data={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'Bearer'}
