import unittest

from bookstore.domain.inventory import OutOfStock, check_available


class InventoryTests(unittest.TestCase):
    def test_exact_stock_is_allowed(self):
        """Граничний випадок: замовлено рівно стільки, скільки є."""
        self.assertIsNone(check_available("Кобзар", 5, 5))

    def test_more_than_stock_is_rejected(self):
        with self.assertRaises(OutOfStock) as ctx:
            check_available("Кобзар", 6, 5)
        self.assertEqual(ctx.exception.available, 4)

    def test_non_positive_quantity_is_rejected(self):
        with self.assertRaises(ValueError):
            check_available("Кобзар", 0, 5)


if __name__ == "__main__":
    unittest.main()
