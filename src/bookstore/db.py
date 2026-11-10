"""Підключення до БД. За замовчуванням SQLite, у продакшені PostgreSQL через DATABASE_URL."""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import StaticPool

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bookstore.db")


class Base(DeclarativeBase):
    pass


def make_engine(url: str = DATABASE_URL):
    if url == "sqlite://":  # БД у пам'яті для тестів: одне спільне з'єднання
        return create_engine(url, connect_args={"check_same_thread": False}, poolclass=StaticPool)
    args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    return create_engine(url, connect_args=args)


def make_session_factory(engine):
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
