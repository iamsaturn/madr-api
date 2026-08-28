from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from madr_api.database import SessionDep
from madr_api.models import User
from madr_api.schemas import Token_Schema
from madr_api.security import create_access_token, verify_password

router = APIRouter(prefix='/auth', tags=['Authorization'])

@router.post('/token', response_model= Token_Schema )
async def post_token(
    session: SessionDep,
    form_data: OAuth2PasswordRequestForm = Depends()):
    user_db = await session.scalar((
        select(User).where(
        User.email == form_data.username
    )))
    if user_db is None:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Invalid credentials')
    
    if not verify_password(
        plain_password= form_data.password,
        hashed_password= user_db.hashed_password): 

        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                            detail='Invalid credentials')

    token = create_access_token({"sub" : user_db.email})
    return{"access_token": token,
           "token_type": "bearer"}