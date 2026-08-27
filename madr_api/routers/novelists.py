from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from madr_api.database import get_session
from madr_api.models import Novelist
from madr_api.schemas import NovelistCreate, NovelistPublic, NovelistUpdate

router = APIRouter(prefix="/novelists", tags=["Novelists"])

SessionDep = Annotated[AsyncSession,Depends(get_session)]

@router.post("/", response_model=NovelistPublic)
async def create_novelist(
    novelist: NovelistCreate, session: SessionDep
):

    novelist_db = Novelist(name=novelist.name)

    session.add(novelist_db)
    await session.commit()
    await session.refresh(novelist_db)
    return novelist_db


@router.get("/", response_model=list[NovelistPublic])
async def get_novelist_list(session: SessionDep):
    query = select(Novelist)
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
):

    query = select(Novelist).where(Novelist.id == novelist_id)
    novelist_db = await session.scalar(query)
    if novelist_db is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Novelist not found"
        )
    update_data = novelist_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(novelist_db, field, value)
    await session.commit()
    await session.refresh(novelist_db)
    return novelist_db


@router.delete("/{novelist_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_novelist(
    novelist_id: int, session: SessionDep
):

    query = select(Novelist).where(Novelist.id == novelist_id)
    novelist_db = await session.scalar(query)
    if novelist_db is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Novelist not found"
        )

    await session.delete(novelist_db)
    await session.commit()
