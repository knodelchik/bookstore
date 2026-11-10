from decimal import Decimal

from pydantic import BaseModel, Field


class BookIn(BaseModel):
    isbn: str
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    price: Decimal
    stock_hall: int = 0
    stock_warehouse: int = 0


class BookOut(BookIn):
    id: int


class OrderItemIn(BaseModel):
    book_id: int
    quantity: int


class OrderIn(BaseModel):
    items: list[OrderItemIn]
    customer_id: int | None = None
    use_bonus: bool = False


class OrderOut(BaseModel):
    id: int
    status: str
    total: Decimal
    bonus_spent: Decimal
