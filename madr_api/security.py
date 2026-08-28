from datetime import UTC, datetime, timedelta
from http import HTTPStatus
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy import select

from madr_api.database import SessionDep
from madr_api.models import User
from madr_api.settings import settings

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

credentials_exception = HTTPException(
    status_code=HTTPStatus.UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:

    return password_hash.verify(plain_password, hashed_password)


def create_access_token(payload: dict) -> str:
    data = payload.copy()
    expiration = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES)
    data.update({"exp": expiration})
    token = jwt.encode(data, settings.SECRET_KEY, settings.ALGORITHM)
    return token


async def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)):

    try:
        decoded_data = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except InvalidTokenError:
        raise credentials_exception
    email = decoded_data.get("sub")
    if email is None:
        raise credentials_exception
    query = select(User).where(User.email == email)
    user = await session.scalar(query)
    if user is None:
        raise credentials_exception
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
