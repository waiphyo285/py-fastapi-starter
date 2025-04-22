from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.db.tenants.resolver import get_db
from app.db.schemas.book import BookCreate, BookRead
from app.services.auth.dependency import jwt_required
from app.services.book import create_book, get_books, get_book_by_id, update_book, delete_book

router = APIRouter(
    dependencies=[Depends(jwt_required)] 
)

@router.post("", response_model=BookRead)
def create(book: BookCreate, db: Session = Depends(get_db)):
    return create_book(db, book)

@router.get("", response_model=list[BookRead])
def get_all(db: Session = Depends(get_db)):
    return get_books(db)

@router.get("/{id}", response_model=BookRead)
def get_by_id(id: int, db: Session = Depends(get_db)):
    db_book = get_book_by_id(db, id)
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return db_book

@router.patch("/{id}", response_model=BookRead)
def update(id: int, book: BookCreate, db: Session = Depends(get_db)):
    updated_book = update_book(db, id, book)
    if not updated_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return updated_book

@router.delete("/{id}", response_model=BookRead)
def delete(id: int, db: Session = Depends(get_db)):
    db_book = delete_book(db, id)
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return db_book