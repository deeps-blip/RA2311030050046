import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_api_schedule(self):
        response = self.client.post("/api/v1/schedule", json={"available_hours": 10})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("selected_tasks", data)
        self.assertIn("total_importance", data)
        self.assertIn("total_duration", data)
        self.assertLessEqual(data["total_duration"], 10)

    def test_api_invalid_input(self):
        response = self.client.post("/api/v1/schedule", json={"available_hours": "invalid"})
        self.assertEqual(response.status_code, 422)

if __name__ == '__main__':
    unittest.main()
