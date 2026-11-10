import unittest

from fastapi.testclient import TestClient

from bookstore.main import create_app

BOOK = {"isbn": "978-617-12-9534-6", "title": "Тіні забутих предків", "author": "Михайло Коцюбинський",
        "price": "250.00", "stock_warehouse": 3}


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(create_app("sqlite://"))

    def test_add_and_search_book(self):
        r = self.client.post("/books", json=BOOK)
        self.assertEqual(r.status_code, 201)
        found = self.client.get("/books", params={"q": "коцюб"}).json()
        self.assertEqual([b["isbn"] for b in found], ["9786171295346"])

    def test_duplicate_isbn_rejected(self):
        self.client.post("/books", json=BOOK)
        self.assertEqual(self.client.post("/books", json=BOOK).status_code, 422)


if __name__ == "__main__":
    unittest.main()
