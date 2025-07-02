from app.controllers._base import BaseController
from app.services.book import book_service
from app.databases.schemas.book import BookCreate, BookRead

router = BaseController(book_service, BookRead, BookCreate).get_router("/book")