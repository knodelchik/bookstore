"""Доступ до даних каталогу."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Book


class BookRepository:
    def __init__(self, session: Session):
        self.s = session

    def add(self, book: Book) -> Book:
        book.refresh_search_key()
        self.s.add(book)
        self.s.flush()
        return book

    def get(self, book_id: int) -> Book | None:
        return self.s.get(Book, book_id)

    def by_isbn(self, isbn: str) -> Book | None:
        return self.s.scalar(select(Book).where(Book.isbn == isbn))

    def search(self, query: str, limit: int = 24) -> list[Book]:
        pattern = f"%{query.casefold()}%"
        stmt = select(Book).where(Book.search_key.like(pattern)).order_by(Book.title).limit(limit)
        return list(self.s.scalars(stmt))
