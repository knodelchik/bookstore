"""Розрахунок суми замовлення, знижок і бонусів (FR-4.2, FR-6.3)."""
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

MAX_BONUS_SHARE = Decimal("0.5")   # бонусами можна оплатити не більше 50 % суми
BONUS_RATE = Decimal("0.05")       # нарахування 5 % від суми позицій без знижки
CENT = Decimal("0.01")


@dataclass(frozen=True)
class Line:
    price: Decimal
    quantity: int
    discount_percent: Decimal = Decimal("0")

    @property
    def total(self) -> Decimal:
        if self.quantity <= 0:
            raise ValueError("Кількість має бути додатною")
        if not Decimal("0") <= self.discount_percent <= Decimal("100"):
            raise ValueError("Знижка має бути від 0 до 100 %")
        gross = self.price * self.quantity
        return (gross * (1 - self.discount_percent / 100)).quantize(CENT, ROUND_HALF_UP)


def order_total(lines: list[Line]) -> Decimal:
    return sum((line.total for line in lines), Decimal("0.00"))


def max_bonus_spend(total: Decimal, available_bonus: Decimal) -> Decimal:
    """Скільки бонусів можна списати: не більше половини суми і не більше наявних."""
    return min(available_bonus, (total * MAX_BONUS_SHARE).quantize(CENT, ROUND_HALF_UP))


def bonus_earned(lines: list[Line]) -> Decimal:
    """Бонуси нараховуються лише за позиції без знижки."""
    base = sum((line.total for line in lines if line.discount_percent == 0), Decimal("0"))
    return (base * BONUS_RATE).quantize(CENT, ROUND_HALF_UP)
