import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor, Movie, Actor,db

#Token to test the unit tests

producer_headers = {
    "Authorization": "Bearer" + "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhUNW9JNF83elRmUndCRVBIa2FnaSJ9.eyJpc3MiOiJodHRwczovL3dlbmthaXRhbi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxZjYyYTkyOGRkYmEwMDM3NDNiYzBkIiwiYXVkIjoiY2FzdGluZyBwcm9qZWN0IiwiaWF0IjoxNTk2MjMxODY2LCJleHAiOjE1OTYzMTgyNjYsImF6cCI6IklLR1BWaVZQWXE1RTJjNlhXaGNUaTVKOU5iVUhSRVBnIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.m93e-3RSsnDsBwAW8VtSJ8OoS9wSyx1sO_2n4ogkRzXyXteoNlrBdkiHe9IhtakAFbJlx6EIjLrC-gwsMnapbpUwEGNac_OxtT4tpak22QGXcuve5JomBPQ6k5kkhXxMUM-s52OFEiyKcyllpbB8vqlGzqaugmdKErSGVzEme6ChHqAfpGytx8BemZD8w-LBxyN08nYZMyOyZAsDIolsxLYX7pdkGygawzLkYYqvEmXJ9LnYXzTQnQfY0k52pIn_8hg9-pUOLIOS0dxOja5L2WlmwtI3qXttACBWHEJgmRpLAWehIzqksX5P6qaeDz0AFYXc_q74Ca_rtSjFB32rCQ"
}

director_headers = {
    "Authorization": "Bearer" + "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhUNW9JNF83elRmUndCRVBIa2FnaSJ9.eyJpc3MiOiJodHRwczovL3dlbmthaXRhbi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxZjYyY2NiYmQ4Y2UwMDNkNjIwNWY0IiwiYXVkIjoiY2FzdGluZyBwcm9qZWN0IiwiaWF0IjoxNTk2MjMwNzIzLCJleHAiOjE1OTYzMTcxMjMsImF6cCI6IklLR1BWaVZQWXE1RTJjNlhXaGNUaTVKOU5iVUhSRVBnIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.UZ8wqri8XDi98ZJRDNn_-dGMyF1EicklEGhVP5zPOsOUSdyVFBG0x8UTdX9D7S-6w8aCA00BXmlKhzz41xScyzjXiEnBr8iPtSUkSh1nIM90CQvcfJD9Mm59vlDKbR-2JQu1Ya9ZxiJFJbtsF6ZgySjo9XcXnU5yCL_kliHtXwq3GjmmrI7iD8Du6XWN1W5icbRmpV8PCNVVjs6ech_G3TM-Eudm7rQZAro8RErlFuDGpV5ExrOF0syBQJDq4pDzAIn9PURTNKDXBg4M4qXtxy9Cu1XiGAKrAjn92BP1mR9ru5c3qlhBDfb5tDdIpqhkIe1jpfTz6HYhzzzxDGYaIQ"
}

assistant_headers = {
    "Authorization": "Bearer" + "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhUNW9JNF83elRmUndCRVBIa2FnaSJ9.eyJpc3MiOiJodHRwczovL3dlbmthaXRhbi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxZjYyODYyOGRkYmEwMDM3NDNiYzBiIiwiYXVkIjoiY2FzdGluZyBwcm9qZWN0IiwiaWF0IjoxNTk2MjMwNjE3LCJleHAiOjE1OTYzMTcwMTcsImF6cCI6IklLR1BWaVZQWXE1RTJjNlhXaGNUaTVKOU5iVUhSRVBnIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.xM1LOa9sFVmqVtL3wXbfO8sB_vawrikEROqQL085J_S2reAMrVEmgab37Y8NFnDgFPydNRgIOlboVFsTbg3vL0VZ3tbro-tr5wRkPfhxrXTqWEYQzuncuJMgw99b24seyrPFtMR8qukK9Yhv7zwraWXVQ29LePEb2N0SBUI2ffFelmj7CK1IUPQIcQdMCE5bnD9eJRqGJsQZ-3oiqR_oq9q32XWoPwvyaWrgetncpQjhqu6DnmCRoFhE-2IFgGTSk4y1-JsytCxfAFscolWn92MuXIywOZk9X1KhcL4-3I2Z9lZ-j8r4y81u3_hPWqvpi3HGifv_kfxgmAiEM3c5Xg"
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