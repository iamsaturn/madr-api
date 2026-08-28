from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from madr_api.database import SessionDep
from madr_api.models import User
from madr_api.schemas import UserCreate, UserPublic, UserUpdate
from madr_api.security import CurrentUserDep, get_password_hash

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserPublic)
async def create_user(user: UserCreate, session: SessionDep):
    if (
        await session.scalar(select(User).where(User.username == user.username))
        is not None
    ):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Username already exists"
        )
    if await session.scalar(select(User).where(User.email == user.email)) is not None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Email already exists"
        )

    user_db = User(
        username=user.username,
        hashed_password=get_password_hash(user.password),
        email=user.email,
    )

    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)
    return user_db


@router.get("/me", response_model=UserPublic)
async def me(
    user: CurrentUserDep,
):
    return user


@router.patch(
    "/me",
    response_model=UserPublic,
)
async def patch_me(
    user_update: UserUpdate, session: SessionDep, current_user: CurrentUserDep
):

    update_data = user_update.model_dump(exclude_unset=True)

    password = update_data.pop("password", None)

    if "username" in update_data:
        query = select(User).where(
            User.username == update_data["username"], User.id != current_user.id
        )
        existing_user = await session.scalar(query)

        if existing_user is not None:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail="Username already exists"
            )

    if "email" in update_data:
        query = select(User).where(
            User.email == update_data["email"], User.id != current_user.id
        )
        existing_user = await session.scalar(query)

        if existing_user is not None:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail="Email already exists"
            )

    if password is not None:
        current_user.hashed_password = get_password_hash(password)

    for field, value in update_data.items():
        setattr(current_user, field, value)
    await session.commit()
    await session.refresh(current_user)
    return current_user


@router.delete("/me", status_code=HTTPStatus.NO_CONTENT)
async def delete_me(session: SessionDep, current_user: CurrentUserDep):
    await session.delete(current_user)
    await session.commit()
