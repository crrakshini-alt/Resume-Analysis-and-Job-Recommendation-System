import unittest
import sys
import os

# Add parent directory to path so we can import services
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.skill_analyser import extract_skills, analyse_skills, SKILLS, JOB_ROLES
from services.interview_question_generator import generate_questions, QUESTION_BANK
from services.answer_evaluator import evaluate_answer, evaluate_answers
from services.video_recommender import recommend_videos, VIDEO_RESOURCES


class TestSkillAnalyser(unittest.TestCase):
    """Unit tests for Resume Skill Extraction and Job Role Matching"""

    def test_extract_skills_found(self):
        sample_text = "Proficient in Python, SQL, Git, and Docker. Experience with Flask."
        extracted = extract_skills(sample_text)
        self.assertIn("python", extracted)
        self.assertIn("sql", extracted)
        self.assertIn("git", extracted)
        self.assertIn("flask", extracted)

    def test_extract_skills_case_insensitive(self):
        sample_text = "PYTHON and jAvAsCrIpT with ReAcT"
        extracted = extract_skills(sample_text)
        self.assertIn("python", extracted)
        self.assertIn("javascript", extracted)
        self.assertIn("react", extracted)

    def test_extract_skills_empty_text(self):
        extracted = extract_skills("")
        self.assertEqual(extracted, [])

    def test_analyse_skills_ranking(self):
        candidate_skills = ["python", "flask", "sql", "git"]
        recommendations = analyse_skills(candidate_skills)
        self.assertTrue(len(recommendations) > 0)
        # Python Developer should be #1 with 100% match
        top_role = recommendations[0]
        self.assertEqual(top_role["job_role"], "Python Developer")
        self.assertEqual(top_role["match_percentage"], 100.0)
        self.assertEqual(len(top_role["missing_skills"]), 0)

    def test_analyse_skills_partial_match(self):
        candidate_skills = ["python", "flask"]
        recommendations = analyse_skills(candidate_skills)
        python_rec = next(r for r in recommendations if r["job_role"] == "Python Developer")
        self.assertEqual(python_rec["match_percentage"], 50.0)
        self.assertIn("sql", python_rec["missing_skills"])
        self.assertIn("git", python_rec["missing_skills"])


class TestInterviewQuestionGenerator(unittest.TestCase):
    """Unit tests for Interview Question Generation based on extracted skills"""

    def test_generate_questions_for_skills(self):
        skills = ["python", "sql"]
        results = generate_questions(skills)
        self.assertEqual(len(results), 2)
        python_group = next(r for r in results if r["skill"] == "python")
        self.assertTrue(len(python_group["questions"]) > 0)
        self.assertIn(python_group["questions"][0], QUESTION_BANK["python"])

    def test_generate_questions_empty_skills(self):
        questions = generate_questions([])
        self.assertEqual(questions, [])

    def test_generate_questions_unknown_skill(self):
        questions = generate_questions(["unknown_nonexistent_skill"])
        self.assertEqual(questions, [])


class TestAnswerEvaluator(unittest.TestCase):
    """Unit tests for Interview Answer Scoring and Evaluation"""

    def test_short_answer_low_score(self):
        question = "What is Python?"
        answer = "A language."
        result = evaluate_answer(question, answer)
        self.assertLess(result["score"], 50)
        self.assertIn("Needs improvement", result["feedback"])

    def test_detailed_relevant_answer_high_score(self):
        question = "What are the main features of Python?"
        answer = (
            "Python is an interpreted, high-level, and dynamically typed programming language. "
            "It supports object-oriented, procedural, and functional programming paradigms, "
            "and has an extensive standard library."
        )
        result = evaluate_answer(question, answer)
        self.assertGreaterEqual(result["score"], 60)
        self.assertIn("Good answer", result["feedback"])

    def test_evaluate_answers_batch(self):
        answers = [
            {"question": "What is Python?", "answer": "Python is a versatile programming language used in web and data science."},
            {"question": "What is SQL?", "answer": "SQL is structured query language used for managing relational databases."}
        ]
        result = evaluate_answers(answers)
        self.assertIn("preparedness_percentage", result)
        self.assertIn("message", result)
        self.assertIn("evaluated_answers", result)
        self.assertEqual(len(result["evaluated_answers"]), 2)
        self.assertGreater(result["preparedness_percentage"], 50.0)


class TestVideoRecommender(unittest.TestCase):
    """Unit tests for Learning Resource & Video Recommendations"""

    def test_recommend_videos_for_missing_skills(self):
        missing = ["python", "react"]
        recs = recommend_videos(missing)
        self.assertEqual(len(recs), 2)
        skills_recommended = [r["skill"] for r in recs]
        self.assertIn("python", skills_recommended)
        self.assertIn("react", skills_recommended)
        self.assertTrue(all("video_url" in r and "video_title" in r for r in recs))

    def test_recommend_videos_empty_list(self):
        recs = recommend_videos([])
        self.assertEqual(recs, [])

    def test_recommend_videos_custom_skill_fallback(self):
        recs = recommend_videos(["kubernetes"])
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0]["skill"], "kubernetes")
        self.assertEqual(recs[0]["video_title"], "Learn kubernetes")
        self.assertIn("youtube.com", recs[0]["video_url"])


if __name__ == "__main__":
    unittest.main()
