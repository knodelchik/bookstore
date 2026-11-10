"""Перевірка ISBN-13 (FR-1.2)."""


class InvalidIsbn(ValueError):
    pass


def normalize_isbn(raw: str) -> str:
    """Прибирає дефіси та пробіли і перевіряє формат і контрольну цифру ISBN-13."""
    digits = raw.replace("-", "").replace(" ", "")
    if len(digits) != 13 or not digits.isdigit():
        raise InvalidIsbn("ISBN-13 має містити рівно 13 цифр")
    if not digits.startswith(("978", "979")):
        raise InvalidIsbn("ISBN-13 має починатися з 978 або 979")
    total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(digits[:12]))
    check = (10 - total % 10) % 10
    if check != int(digits[12]):
        raise InvalidIsbn(f"Неправильна контрольна цифра: очікується {check}")
    return digits
