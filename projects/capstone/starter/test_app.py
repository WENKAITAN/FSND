import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor, Movie, Actor,db

#Token to test the unit tests

producer_headers = {
    "Authorization": "Bearer" + "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhUNW9JNF83elRmUndCRVBIa2FnaSJ9.eyJpc3MiOiJodHRwczovL3dlbmthaXRhbi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxZjYyYTkyOGRkYmEwMDM3NDNiYzBkIiwiYXVkIjoiY2FzdGluZyBwcm9qZWN0IiwiaWF0IjoxNTk2MzE4MTA0LCJleHAiOjE1OTY0MDQ1MDQsImF6cCI6IklLR1BWaVZQWXE1RTJjNlhXaGNUaTVKOU5iVUhSRVBnIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.gINRtEY2SwYO1jooShF73afc6eEMYTsZII2b8RZHPjAnaDnmIMoBdOH1JJlzvU7nz6XuCZqrCNzugTu9DM2azL-3bPhlpmAQaY5-XpodJeUotLWhfBlIQnnG5MwwadtHg8MnbojQRUJFEWt_t-teUVm586KxpW8zj8CdTfq2o-9nDUK-WZfhNh7xDOHodKU3ZdcH0UIepQR0rZj4Cqr-PfbCznlpiQqBZHXZXdu5wte_Nitw6o0rynGCqRaSgR32S9GL-yr51zxx-RegYUqILF5R3EPMl9SWU5ka4JQXUwejKf7jEqOH_dagM5ZAW7jl1UZRv8AAg0nQ5UrHZpiEDA"
}

director_headers = {
    "Authorization": "Bearer" + "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhUNW9JNF83elRmUndCRVBIa2FnaSJ9.eyJpc3MiOiJodHRwczovL3dlbmthaXRhbi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxZjYyY2NiYmQ4Y2UwMDNkNjIwNWY0IiwiYXVkIjoiY2FzdGluZyBwcm9qZWN0IiwiaWF0IjoxNTk2MzE4MDcxLCJleHAiOjE1OTY0MDQ0NzEsImF6cCI6IklLR1BWaVZQWXE1RTJjNlhXaGNUaTVKOU5iVUhSRVBnIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.NNJClQjYw7m2RY7Qq1GduPu7vthAIYozmW8k6KomOexVR2xL2aez9063eF5aAP5J3IIuxQU4_pE0__C54fAXivC1rnSJadUzX_6zBl_IiyiStdCTNBM4_KsBxRmmNM0XPX7jdKh1h1oJAznqQVwTWRCA8A1ivauHZIdHy1VIKyTadJKemydeYDyjhtDlfktwTrWDgJ0uVEIk7vzBp16LOwDLEevmozXQayA4x_7yQ54BpFbhEnWdezrt0ljyBYnWf6klGO3tZAZwuMNyEcxbfaa3o8s0wnpWCFDLlBJb-Gc1cmImaREk192X4yDr71OU6qn-90UTmnJQn3x82qEHUw"
}

assistant_headers = {
    "Authorization": "Bearer" + "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhUNW9JNF83elRmUndCRVBIa2FnaSJ9.eyJpc3MiOiJodHRwczovL3dlbmthaXRhbi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxZjYyODYyOGRkYmEwMDM3NDNiYzBiIiwiYXVkIjoiY2FzdGluZyBwcm9qZWN0IiwiaWF0IjoxNTk2MzE4MDI1LCJleHAiOjE1OTY0MDQ0MjUsImF6cCI6IklLR1BWaVZQWXE1RTJjNlhXaGNUaTVKOU5iVUhSRVBnIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.r5Vjc5k0vLrp3kByr__AKUKLeWxr38_aLrvbHlUqBCLwphk1sBXvElB4OMccb46OmEzzg2usA9VDMi7HDFRzimbTjynavm-VyLGTN7gpJOcDR__ss7CldztGb4GQaTEmO5pEZKFuWVhaEWcvAHxpJi4EH590FE3Az7bErSQncPk1UPofWqhEFV5fAQISLkTTRo7oaIZsMRSezq_UPcuPwJEfkUSpu0WaH5epvDND6VTCiYlXK9n7eswGCtw1xqmf2oORztT60R9dlpvoV0aTM2eJO-Cc34uDNtMWwqDp5rXUq_is2lLY3gqTD-Xa6MdMpok2bxH6ZflX_BWM9F92tQ"
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
            'release_date': "2020-07-31",
        }

        self.new_actor = {
            'name': 'test_actor',
            'age': 20,
            'gender': 'Male',
            'movie_id': 1
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
        res = self.client().get('movies', headers=assistant_headers)
        data = json.loads(res.data.decode('utf-8'))
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    
    def test_get_actors(self):
        res = self.client().get('/actors', headers=assistant_headers)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_actors_fail(self):
        res = self.client().get('/actors', headers=assistant_headers)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_post_movies(self):
        res = self.client().post('/movies', json=self.new_movie, headers=director_headers)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_movie']['title'], "test_movie")

    def test_post_actor(self):
        res = self.client().post('/actors', json=self.new_actor, headers=director_headers)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_movie']['age'], 20)

    def test_patch_movie(self):
        res = self.client().patch('/movies/3', json=self.new_movie, headers=producer_headers)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated_movie']['title'], "test_movie")
    
    def test_patch_movie_fail(self):
        res = self.client().patch('/movies/6', json=self.new_movie, headers=director_headers)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_patch_actor(self):
        res = self.client().patch('/actors/4', json=self.new_actor, headers=producer_headers)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated_actor']['name'], "test_actor")

    def test_patch_actor_fail(self):
        res = self.client().patch('/actors/100', json=self.new_actor, headers=producer_headers)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_movie(self):
        res = self.client().delete('/movies/3', headers=producer_headers)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
    def test_delete_movie_fail(self):
        res = self.client().delete('/movies/200', headers=producer_headers)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_actor(self):
        res = self.client().delete('/actors/1', headers=producer_headers)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
    def test_delete_actor_fail(self):
        res = self.client().delete('/actors/200', headers=producer_headers)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

          
if __name__ == "__main__":
    unittest.main()