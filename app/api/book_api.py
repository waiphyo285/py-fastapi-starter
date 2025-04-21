from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.db.book_schema import BookCreate, BookRead
from app.services.book_service import create_book, get_books, get_book, delete_book

book_router = APIRouter()

@book_router.post("", response_model=BookRead)
def create(book: BookCreate, db: Session = Depends(get_db)):
    return create_book(db, book)

@book_router.get("", response_model=list[BookRead])
def get_all(db: Session = Depends(get_db)):
    return get_books(db)

@book_router.get("/{id}", response_model=BookRead)
def get_by_id(id: int, db: Session = Depends(get_db)):
    db_book = get_book(db, id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@book_router.delete("/{id}", response_model=BookRead)
def delete(id: int, db: Session = Depends(get_db)):
    db_book = delete_book(db, id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book