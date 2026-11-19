import unittest
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import database
from app import app

class TestAPIEndpoints(unittest.TestCase):
    """Integration and Functional API Tests for Resume Analyser"""

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()

    def setUp(self):
        # Configure a fresh isolated test database for each test
        self.test_db = "test_api_database.db"
        database.DATABASE_NAME = self.test_db
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        database.create_tables()

    def tearDown(self):
        if os.path.exists(self.test_db):
            try:
                os.remove(self.test_db)
            except PermissionError:
                pass

    # --- Home & Health Checks ---
    def test_home_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "success")

    def test_health_check(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "success")
        self.assertIn("running", data["message"].lower())

    # --- User Registration Tests ---
    def test_register_success(self):
        payload = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "password": "strongPassword123"
        }
        response = self.client.post("/api/register", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["status"], "success")

    def test_register_duplicate_email(self):
        payload = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "password": "strongPassword123"
        }
        self.client.post("/api/register", json=payload)
        # Duplicate registration attempt
        response = self.client.post("/api/register", json=payload)
        self.assertEqual(response.status_code, 409)
        data = response.get_json()
        self.assertEqual(data["status"], "error")
        self.assertIn("already registered", data["message"].lower())

    def test_register_short_password(self):
        payload = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "password": "short"
        }
        response = self.client.post("/api/register", json=payload)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("at least 8 characters", data["message"])

    def test_register_missing_fields(self):
        payload = {"name": "Jane Doe"}
        response = self.client.post("/api/register", json=payload)
        self.assertEqual(response.status_code, 400)

    # --- User Login Tests ---
    def test_login_success(self):
        # First register
        self.client.post("/api/register", json={
            "name": "Alice Bob",
            "email": "alice@example.com",
            "password": "password123"
        })
        # Login
        response = self.client.post("/api/login", json={
            "email": "alice@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "success")
        self.assertIn("user", data)
        self.assertEqual(data["user"]["email"], "alice@example.com")

    def test_login_invalid_password(self):
        self.client.post("/api/register", json={
            "name": "Alice Bob",
            "email": "alice@example.com",
            "password": "password123"
        })
        response = self.client.post("/api/login", json={
            "email": "alice@example.com",
            "password": "wrongPassword"
        })
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertEqual(data["status"], "error")

    def test_login_nonexistent_user(self):
        response = self.client.post("/api/login", json={
            "email": "unknown@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 401)

    # --- Interview Evaluation Tests ---
    def test_evaluate_interview_success(self):
        # Register user first
        reg = self.client.post("/api/register", json={
            "name": "Test User",
            "email": "test@user.com",
            "password": "password123"
        })
        login_res = self.client.post("/api/login", json={
            "email": "test@user.com",
            "password": "password123"
        })
        user_id = login_res.get_json()["user"]["id"]

        eval_payload = {
            "user_id": user_id,
            "questions": ["What is Python?"],
            "answers": [
                {"question": "What is Python?", "answer": "Python is a high-level programming language used widely in data science."}
            ]
        }
        response = self.client.post("/api/evaluate-interview", json=eval_payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "success")
        self.assertIn("evaluation", data)

    def test_evaluate_interview_invalid_user(self):
        eval_payload = {
            "user_id": 99999,
            "questions": ["What is Python?"],
            "answers": [{"question": "What is Python?", "answer": "A language."}]
        }
        response = self.client.post("/api/evaluate-interview", json=eval_payload)
        self.assertEqual(response.status_code, 404)

    # --- Resume Analysis Validation Tests ---
    def test_analyze_resume_no_file(self):
        response = self.client.post("/api/analyze-resume")
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("no resume uploaded", data["message"].lower())


if __name__ == "__main__":
    unittest.main()
