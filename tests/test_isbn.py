import unittest

from bookstore.domain.isbn import InvalidIsbn, normalize_isbn


class IsbnTests(unittest.TestCase):
    def test_valid_isbn_with_hyphens(self):
        self.assertEqual(normalize_isbn("978-617-12-9534-6"), "9786171295346")

    def test_wrong_check_digit(self):
        with self.assertRaises(InvalidIsbn):
            normalize_isbn("9786171295345")

    def test_too_short(self):
        with self.assertRaises(InvalidIsbn):
            normalize_isbn("978617129")


if __name__ == "__main__":
    unittest.main()
