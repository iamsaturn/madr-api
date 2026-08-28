from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select


from madr_api.database import SessionDep
from madr_api.models import User
from madr_api.schemas import UserCreate, UserPublic
from madr_api.security import CurrentUserDep, get_password_hash

router = APIRouter(prefix='/users', tags=['Users'])

@router.post('/',response_model=UserPublic)
async def create_user(user: UserCreate, session: SessionDep):
    if await session.scalar(
        select(User).where(User.username == user.username)
    ) is not None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username already exists')
    if await session.scalar(
            select(User).where(User.email == user.email)
        ) is not None:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already exists')
    
    user_db = User(
        username= user.username,
        hashed_password= get_password_hash(user.password),
        email= user.email
    )

    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)
    return user_db

@router.get('/me', response_model=UserPublic)
async def me(user: CurrentUserDep, ):
     return user