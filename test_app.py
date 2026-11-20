import unittest
from app import app, compare_text


class TestTextDifferenceChecker(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_identical_text(self):
        result = compare_text("Hello", "Hello")
        self.assertEqual(result, ["  Hello"])

    def test_different_text(self):
        result = compare_text("Hello", "Hi")
        self.assertIn("- Hello", result)
        self.assertIn("+ Hi", result)

    def test_homepage(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 500)

    def test_compare_api(self):
        response = self.client.post("/compare", json={
            "original": "Hello",
            "modified": "Hi"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("+ Hi", response.get_json()["differences"])

    def test_invalid_input(self):
        response = self.client.post("/compare", json={
            "original": 123,
            "modified": "Hello"
        })
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
