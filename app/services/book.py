from sqlalchemy.orm import Session
from app.db.models.book import Book
from app.db.schemas.book import BookCreate

def create_book(db: Session, book: BookCreate):
    new_book = Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

def get_books(db: Session):
    return db.query(Book).all()

def get_book_by_id(db: Session, id: int):
    return db.query(Book).filter(Book.id == id).first()

def update_book(db: Session, id: int, book_data: BookCreate):
    book = get_book_by_id(db, id)
    if book: 
        for key, value in book_data.model_dump().items():
            setattr(book, key, value)
        db.commit()
        db.refresh(book)
    return book

def delete_book(db: Session, id: int):
    book = get_book_by_id(db, id)
    if book:
        db.delete(book)
        db.commit()
    return book