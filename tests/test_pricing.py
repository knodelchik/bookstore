import unittest
from decimal import Decimal as D

from bookstore.domain.pricing import Line, bonus_earned, max_bonus_spend, order_total


class PricingTests(unittest.TestCase):
    def test_order_total_with_discount(self):
        lines = [Line(D("250.00"), 2), Line(D("400.00"), 1, D("10"))]
        self.assertEqual(order_total(lines), D("860.00"))

    def test_bonus_limited_to_half_of_total(self):
        self.assertEqual(max_bonus_spend(D("300.00"), D("1000")), D("150.00"))

    def test_bonus_not_more_than_available(self):
        self.assertEqual(max_bonus_spend(D("300.00"), D("20")), D("20"))

    def test_no_bonus_for_discounted_lines(self):
        lines = [Line(D("200.00"), 1), Line(D("100.00"), 1, D("50"))]
        self.assertEqual(bonus_earned(lines), D("10.00"))

    def test_zero_quantity_rejected(self):
        with self.assertRaises(ValueError):
            _ = Line(D("100"), 0).total


if __name__ == "__main__":
    unittest.main()
