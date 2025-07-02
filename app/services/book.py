
from app.services._base import BaseService
from app.databases.models.book import Book
from app.databases.schemas.book import BookCreate

book_service = BaseService[Book, BookCreate](Book)