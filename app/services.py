from models import *
from fastapi import HTTPException
from sqlmodel import Session, select

def get_user(db: Session, user_id: str) -> User :
    return __get(db, user_id, User)

def get_book(db: Session, book_id: int):
    return __get(db, book_id, Book)

def get_books(db: Session, book_ids: list[int]):
    return db.exec(select(Book).where(Book.id.in_(book_ids))).all()

def __get(db: Session, id, model):
    item = db.get(model, id)
    if not item:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return item