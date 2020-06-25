import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_not_found(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_question(self):
        total_questions_before = len(Question.query.all())
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)
        total_questions_after = len(Question.query.all())

        self.assertEqual(res.status_code,200)
        self.assertEqual(total_questions_before,total_questions_after+1)
        self.assertEqual(data['success'], True)
    
    def test_delete_question_failure(self):
        total_questions_before = len(Question.query.all())
        res = self.client().delete('/questions/2000')
        data = json.loads(res.data)
        total_questions_after = len(Question.query.all())

        self.assertEqual(res.status_code, 404)
        self.assertEqual(total_questions_before,total_questions_after)
        self.assertEqual(data['success'], False)

    def test_create_questions(self):
        new_question = {
            'question': 'new question',
            'answer': 'new answer',
            'difficulty': 1,
            'category': 1
        }
        total_questions_before = len(Question.query.all())
        res = self.client().post('/questions/new', json=new_question)
        data = json.loads(res.data)
        total_questions_after = len(Question.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(total_questions_after, total_questions_before + 1)

    def test_create_question_falure(self):
        new_question = {
            'question': 'new question',
            'answer': 'new answer',
            'category': ""
        }
        total_questions_before = len(Question.query.all())
        res = self.client().post('/questions/new', json=new_question)
        data = json.loads(res.data)
        total_questions_after = len(Question.query.all())

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(total_questions_after, total_questions_before)
    
    def test_search_question_not_found(self):
        searchTerm = {
            "searchTerm":"movie"
        }
        res = self.client().post('/questions/search', json=searchTerm)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(data['success'], False)
    
    def test_search_question(self):
        searchTerm = {
            "searchTerm":""
        }
        res = self.client().post('/questions/search', json=searchTerm)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_question_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
    
    def test_get_question_by_category_not_found(self):
        res = self.client().get('/categories/10/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")    

    def test_play_quiz(self):
        new_quiz_round = {'previous_questions': [],
                          'quiz_category': {'type': 'Entertainment', 'id': 5}}

        res = self.client().post('/quizzes', json=new_quiz_round)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_play_quiz_unprocessable(self):
        new_quiz_round = {'previous_questions': []}

        res = self.client().post('/quizzes', json=new_quiz_round)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()