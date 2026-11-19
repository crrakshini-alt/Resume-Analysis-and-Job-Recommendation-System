import unittest
import sqlite3
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import database

class TestDatabase(unittest.TestCase):
    """Database Unit Tests for Schema and Constraints"""

    def setUp(self):
        # Use an in-memory database or a temporary test database
        self.test_db = "test_database.db"
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

    def test_tables_created(self):
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row["name"] for row in cursor.fetchall()]
        conn.close()

        self.assertIn("users", tables)
        self.assertIn("resumes", tables)
        self.assertIn("resume_analysis", tables)
        self.assertIn("interview_attempts", tables)

    def test_user_insertion_and_query(self):
        conn = database.get_db_connection()
        conn.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            ("John Doe", "john@example.com", "hashed_pw")
        )
        conn.commit()

        user = conn.execute("SELECT * FROM users WHERE email = ?", ("john@example.com",)).fetchone()
        conn.close()

        self.assertIsNotNone(user)
        self.assertEqual(user["name"], "John Doe")
        self.assertEqual(user["email"], "john@example.com")

    def test_duplicate_email_constraint(self):
        conn = database.get_db_connection()
        conn.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            ("User 1", "test@example.com", "pass1")
        )
        conn.commit()

        # Duplicate email must raise sqlite3.IntegrityError
        with self.assertRaises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                ("User 2", "test@example.com", "pass2")
            )
            conn.commit()
        conn.close()

    def test_interview_attempt_insertion(self):
        conn = database.get_db_connection()
        cursor = conn.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            ("Candidate", "cand@test.com", "pass123")
        )
        user_id = cursor.lastrowid
        conn.commit()

        conn.execute(
            """INSERT INTO interview_attempts (user_id, questions, answers, preparedness_percentage)
               VALUES (?, ?, ?, ?)""",
            (user_id, "['Q1']", "['A1']", 85.5)
        )
        conn.commit()

        attempt = conn.execute("SELECT * FROM interview_attempts WHERE user_id = ?", (user_id,)).fetchone()
        conn.close()

        self.assertIsNotNone(attempt)
        self.assertEqual(attempt["preparedness_percentage"], 85.5)


if __name__ == "__main__":
    unittest.main()
