from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select

from madr_api.database import SessionDep
from madr_api.models import Novelist
from madr_api.schemas import (
    NovelistCreate,
    NovelistFilter,
    NovelistPublic,
    NovelistUpdate,
)
from madr_api.security import CurrentUserDep

router = APIRouter(prefix="/novelists", tags=["Novelists"])
NovelistFilterDep = Annotated[NovelistFilter, Query()]


@router.post("/", response_model=NovelistPublic)
async def create_novelist(
    novelist: NovelistCreate, session: SessionDep, current_user: CurrentUserDep
):
    query = select(Novelist).where(Novelist.name == novelist.name)
    existing_novelist = await session.scalar(query)
    if existing_novelist is not None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Novelist already exists"
        )
    novelist_db = Novelist(name=novelist.name)

    session.add(novelist_db)
    await session.commit()
    await session.refresh(novelist_db)
    return novelist_db


@router.get("/", response_model=list[NovelistPublic])
async def get_novelist_list(session: SessionDep, filter: NovelistFilterDep):
    query = select(Novelist)

    if filter.name is not None:
        query = query.where(Novelist.name.ilike(f"%{filter.name}%"))

    query = query.offset(filter.offset).limit(filter.limit).order_by(Novelist.id)

    result = await session.scalars(query)
    novelist_list = result.all()
    return novelist_list


@router.get("/{novelist_id}", response_model=NovelistPublic)
async def get_novelist(novelist_id: int, session: SessionDep):
    query = select(Novelist).where(Novelist.id == novelist_id)
    novelist_db = await session.scalar(query)
    if novelist_db is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Novelist not found"
        )
    return novelist_db


@router.patch("/{novelist_id}", response_model=NovelistPublic)
async def patch_novelist(
    novelist_id: int,
    novelist_update: NovelistUpdate,
    session: SessionDep,
    current_user: CurrentUserDep,
):
    query = select(Novelist).where(Novelist.id == novelist_id)
    novelist_db = await session.scalar(query)
    if novelist_db is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Novelist not found"
        )
    update_data = novelist_update.model_dump(exclude_unset=True)
    if "name" in update_data:
        query = select(Novelist).where(
            Novelist.name == update_data["name"], Novelist.id != novelist_id
        )
        existing_novelist = await session.scalar(query)
        if existing_novelist is not None:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail="Novelist already exists"
            )

    for field, value in update_data.items():
        setattr(novelist_db, field, value)
    await session.commit()
    await session.refresh(novelist_db)
    return novelist_db


@router.delete("/{novelist_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_novelist(
    novelist_id: int, session: SessionDep, current_user: CurrentUserDep
):

    query = select(Novelist).where(Novelist.id == novelist_id)
    novelist_db = await session.scalar(query)
    if novelist_db is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Novelist not found"
        )

    await session.delete(novelist_db)
    await session.commit()
