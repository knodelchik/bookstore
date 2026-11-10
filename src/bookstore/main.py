"""Точка входу FastAPI: рівень представлення (REST API)."""
from collections.abc import Iterator

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import __version__
from .api.schemas import BookIn, BookOut
from .db import Base, make_engine, make_session_factory
from .domain.isbn import InvalidIsbn
from .repositories.books import BookRepository
from .services.catalog import CatalogService, DuplicateIsbn


def create_app(database_url: str | None = None) -> FastAPI:
    engine = make_engine(database_url) if database_url else make_engine()
    Base.metadata.create_all(engine)
    SessionLocal = make_session_factory(engine)
    app = FastAPI(title="Книгарня API", version=__version__)

    def session() -> Iterator[Session]:
        with SessionLocal() as s:
            with s.begin():
                yield s

    @app.get("/health")
    def health():
        return {"status": "ok", "version": __version__}

    @app.post("/books", response_model=BookOut, status_code=201)
    def add_book(data: BookIn, s: Session = Depends(session)):
        try:
            return CatalogService(BookRepository(s)).add_book(**data.model_dump())
        except (InvalidIsbn, DuplicateIsbn, ValueError) as e:
            raise HTTPException(422, str(e))

    @app.get("/books", response_model=list[BookOut])
    def search(q: str = "", s: Session = Depends(session)):
        return CatalogService(BookRepository(s)).search(q)

    return app


app = create_app()
