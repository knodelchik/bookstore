"""Доступ до даних замовлень і клієнтів."""
from sqlalchemy.orm import Session

from ..models import Customer, Order


class OrderRepository:
    def __init__(self, session: Session):
        self.s = session

    def add(self, order: Order) -> Order:
        self.s.add(order)
        self.s.flush()
        return order

    def get(self, order_id: int) -> Order | None:
        return self.s.get(Order, order_id)

    def customer(self, customer_id: int) -> Customer | None:
        return self.s.get(Customer, customer_id)
