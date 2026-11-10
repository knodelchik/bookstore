"""Оформлення замовлення (F3): залишки, сума, бонуси."""
from decimal import Decimal

from ..domain.inventory import check_available
from ..domain.pricing import Line, bonus_earned, max_bonus_spend, order_total
from ..models import Order, OrderItem
from ..repositories.books import BookRepository
from ..repositories.orders import OrderRepository


class OrderService:
    def __init__(self, books: BookRepository, orders: OrderRepository):
        self.books, self.orders = books, orders

    def place(self, items: list[tuple[int, int]], customer_id: int | None = None,
              use_bonus: bool = False) -> Order:
        if not items:
            raise ValueError("Кошик порожній")
        lines, rows = [], []
        for book_id, qty in items:
            book = self.books.get(book_id)
            if book is None:
                raise LookupError(f"Книгу {book_id} не знайдено")
            check_available(book.title, qty, book.stock_warehouse)
            lines.append(Line(Decimal(book.price), qty))
            rows.append((book, qty))
        total = order_total(lines)
        spent = Decimal("0")
        customer = self.orders.customer(customer_id) if customer_id else None
        if customer and use_bonus:
            spent = max_bonus_spend(total, Decimal(customer.bonus))
            customer.bonus = Decimal(customer.bonus) - spent
        if customer:
            customer.bonus = Decimal(customer.bonus) + bonus_earned(lines)
        order = Order(customer_id=customer_id, total=total - spent, bonus_spent=spent)
        for book, qty in rows:
            book.stock_warehouse -= qty
            order.items.append(OrderItem(book_id=book.id, quantity=qty, price=book.price))
        return self.orders.add(order)
