import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor, Movie, Actor,db

#Token to test the unit tests

producer_headers = {
    "Authorization": "Bearer " + "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhUNW9JNF83elRmUndCRVBIa2FnaSJ9.eyJpc3MiOiJodHRwczovL3dlbmthaXRhbi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxZjYyYTkyOGRkYmEwMDM3NDNiYzBkIiwiYXVkIjoiY2FzdGluZyBwcm9qZWN0IiwiaWF0IjoxNTk2NDk4MjE0LCJleHAiOjE1OTY1ODQ2MTQsImF6cCI6IklLR1BWaVZQWXE1RTJjNlhXaGNUaTVKOU5iVUhSRVBnIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.QqiS2SRBU2S28fJI1zHGaemGysw2_eNpb8iJGG-wKwcS0sz4VlVVucNG2A0uRHJQDCeKIFxyZwq5It0_ljlxzDArtkrCrj6JGsgNTMDEPR3tMxP2CQGQjaq-qEEIXt2vDH-He-b4P0P5Tojko5J8IwNaLca5ZtfcA8k_RXe_91_OimowGJwNOckIV9JGFv_9M1q80ltXsmeBiWl8tolcLsdaE7AKQrOIdRG66R3kC7AJa-c7qYZA6SFtFNTK8SrwcUgHwflxwQSjEKTBrbhdtpYWnIMoLXT9NUeMRAGhDpmYDZ9DQcciixa_Yg1pKekH8TeZ8JaZlsiChZrocu19Ng"
}

director_headers = {
    "Authorization": "Bearer " + "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhUNW9JNF83elRmUndCRVBIa2FnaSJ9.eyJpc3MiOiJodHRwczovL3dlbmthaXRhbi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxZjYyY2NiYmQ4Y2UwMDNkNjIwNWY0IiwiYXVkIjoiY2FzdGluZyBwcm9qZWN0IiwiaWF0IjoxNTk2NDk4MTI2LCJleHAiOjE1OTY1ODQ1MjYsImF6cCI6IklLR1BWaVZQWXE1RTJjNlhXaGNUaTVKOU5iVUhSRVBnIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.EYXYCuGeBf9i70KrIAFyeqBs-WJmkq5KPp48SZQ6PLCUFj8bJxWjVd2fYCRvUuup0K0ikpXD0QI5uXMqBYcKcwYT5KAmmVYR1-bB-I4HFwa56kmXGzyedv5n6hmarDM9ZlnnP0VjD8YXdjm-RHHp46_QcPUvDuPe_wsJtcZy0590BEA1smQgJV8VuMzor_pSRjEDGlyjcSQVRNhJyUgIzAdXLUMAYlgIKYsHRaItL9fKFEeiV9huReY0O9BwJch-hIMzYdOuSJcwuSAbZ7dEeG-ERCnwJuEsK98pv3y_aYdmkCy9dG4UH28VKgfg6bktJRITKdAZ-JAwAPnc1myHWQ"
}

assistant_headers = {
    "Authorization": "Bearer " + "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhUNW9JNF83elRmUndCRVBIa2FnaSJ9.eyJpc3MiOiJodHRwczovL3dlbmthaXRhbi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxZjYyODYyOGRkYmEwMDM3NDNiYzBiIiwiYXVkIjoiY2FzdGluZyBwcm9qZWN0IiwiaWF0IjoxNTk2NDk4MDkxLCJleHAiOjE1OTY1ODQ0OTEsImF6cCI6IklLR1BWaVZQWXE1RTJjNlhXaGNUaTVKOU5iVUhSRVBnIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.xZ7g7E1L0RIi6OYdlbRWDiy1bSbshTEHswV5cvh-lPCgs4TKc0h_fgSGQLVhpXbYy3zeNU-ty50TrNmKKXftj6z_WrbbR6JZUmpein4vWDsTYM8AjZlekBhhObrhG7taO3xkrkz97_IiKtoyXtnwXUJ3HuOYFpSsKL9ek2U7YL2gmSPIpryCxFXQiPzuzkuYwsQoQ1MI2sPnvbyU95rzd6HakB3h4ue3Tl7Dnoa9EFz_Z3SULY9bUgYYKYhgWOrBrg1xCpo_q4LbOFMHSyVTaN7vd50b3CRvylO5wG7aCxeCQajx5OfG3TrqDthMlQ1PIaKq3LPZ6aHU6xVWzJgiWA"
}

class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)
        db.create_all()

        self.new_movie = {
            'title': 'test_movie',
            'release_date': "2020-07-31"
        }

        self.new_actor = {
            'name': 'test_actor',
            'age': 20,
            'gender': 'Male'
        }
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()


    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_movies(self):
        res = self.client().get('/movies', headers=assistant_headers)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_movies_fail(self):
        res = self.client().get('movies')
        data = json.loads(res.data.decode('utf-8'))
        
        self.assertEqual(res.status_code, 401)
    
    def test_get_actors(self):
        res = self.client().get('/actors', headers=assistant_headers)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_actors_fail(self):
        res = self.client().get('/actors')
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 401)

    def test_post_movies(self):
        res = self.client().post('/movies', json=self.new_movie, headers=producer_headers)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_movie']['title'], "test_movie")

    def test_post_actor(self):
        res = self.client().post('/actors', json=self.new_actor, headers=director_headers)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data["new_actor"]['age'], 20)

    def test_patch_movie(self):
        res = self.client().patch('/movies/11', json=self.new_movie, headers=producer_headers)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated_movie']['title'], "test_movie")
    
    def test_patch_movie_fail(self):
        res = self.client().patch('/movies/100', json=self.new_movie, headers=director_headers)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_patch_actor(self):
        res = self.client().patch('/actors/10', json=self.new_actor, headers=producer_headers)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated_actor']['name'], "test_actor")

    def test_patch_actor_fail(self):
        res = self.client().patch('/actors/100', json=self.new_actor, headers=producer_headers)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)

    def test_delete_movie(self):
        res = self.client().delete('/movies/9', headers=producer_headers)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_delete_movie_fail(self):
        res = self.client().delete('/movies/200', headers=producer_headers)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_actor(self):
        res = self.client().delete('/actors/6', headers=producer_headers)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
    def test_delete_actor_fail(self):
        res = self.client().delete('/actors/200', headers=producer_headers)
        data = json.loads(res.data.decode('utf-8'))
        
        self.assertEqual(data['success'], False)

          
if __name__ == "__main__":
    unittest.main()