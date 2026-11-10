"""Перевірка залишків (FR-3.2, FR-5.7)."""


class OutOfStock(Exception):
    def __init__(self, title: str, requested: int, available: int):
        super().__init__(f"«{title}»: замовлено {requested}, доступно {available}")
        self.available = available


def check_available(title: str, requested: int, available: int) -> None:
    if requested <= 0:
        raise ValueError("Кількість має бути додатною")
    if requested > available:
        raise OutOfStock(title, requested, available)
