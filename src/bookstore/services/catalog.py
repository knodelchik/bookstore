"""Бізнес-логіка каталогу (F1, F2)."""
from decimal import Decimal

from ..domain.isbn import normalize_isbn
from ..models import Book
from ..repositories.books import BookRepository


class DuplicateIsbn(ValueError):
    pass


class CatalogService:
    def __init__(self, books: BookRepository):
        self.books = books

    def add_book(self, isbn: str, title: str, author: str, price: Decimal,
                 stock_hall: int = 0, stock_warehouse: int = 0) -> Book:
        isbn = normalize_isbn(isbn)
        if self.books.by_isbn(isbn):
            raise DuplicateIsbn(f"Книга з ISBN {isbn} вже є в каталозі")
        if price <= 0:
            raise ValueError("Ціна має бути додатною")
        return self.books.add(Book(isbn=isbn, title=title, author=author, price=price,
                                   stock_hall=stock_hall, stock_warehouse=stock_warehouse))

    def search(self, query: str) -> list[Book]:
        query = query.strip()
        return self.books.search(query) if query else []
