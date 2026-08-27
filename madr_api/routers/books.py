from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from madr_api.database import get_session
from madr_api.models import Book, Novelist
from madr_api.schemas import BookCreate, BookPublic, BookUpdate

router = APIRouter(prefix='/books',tags=['Books'])

SessionDep = Annotated[AsyncSession, Depends(get_session)]

@router.post('/', response_model=BookPublic)
async def post_book (book: BookCreate, session:SessionDep):
    query = select(Novelist).where(Novelist.id == book.novelist_id)
    novelist_db = await session.scalar(query)
    if novelist_db is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='Novelist not found')

    book_db = Book(
        title=book.title,
        year=book.year,
        novelist=novelist_db
    )
    session.add(book_db)
    await session.commit()
    return book_db

@router.get('/',response_model=list[BookPublic])
async def get_books(session: SessionDep):
    query = select(Book).options(selectinload(Book.novelist))
    result = await session.scalars(query)
    book_list = result.all()
    return book_list

@router.get('/{book_id}', response_model=BookPublic)
async def get_book_by_id(book_id: int, session: SessionDep):
    query = select(Book).options(
        selectinload(Book.novelist)).where(
            Book.id == book_id
        )
    book_db = await session.scalar(query)
    if book_db is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Book not found')
    return book_db

@router.patch('/{book_id}', response_model=BookPublic)
async def patch_book(
    book_id: int,
    book_patch:BookUpdate,
    session:SessionDep):
    query = select(Book).options(
        selectinload(Book.novelist)
    ).where(Book.id == book_id)
    book_db = await session.scalar(query)
    if book_db is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Book not found')
    update_data = book_patch.model_dump(exclude_unset=True)
    novelist_id = update_data.pop('novelist_id',None)
    if novelist_id is not None:
        query = select(Novelist).where(Novelist.id == novelist_id)
        novelist_db = await session.scalar(query)
        if novelist_db is None:
            raise HTTPException(
                         status_code=HTTPStatus.NOT_FOUND,
                         detail='Novelist not found')
        book_db.novelist = novelist_db
    for field, value in update_data.items():
         setattr(book_db,field,value)

    await session.commit()
    return book_db

@router.delete('/{book_id}',status_code=HTTPStatus.NO_CONTENT)
async def delete_book(
    book_id: int,
    session:SessionDep):
    query = select(Book).where(Book.id == book_id)
    book_db = await session.scalar(query)
    if book_db is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Book not found')
    await session.delete(book_db)
    await session.commit()