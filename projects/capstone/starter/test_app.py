import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor, Movie, Actor

#Token to test the unit tests

producer_headers = {
    "Authorization": "Bearer" + "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhUNW9JNF83elRmUndCRVBIa2FnaSJ9.eyJpc3MiOiJodHRwczovL3dlbmthaXRhbi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxZjYyYTkyOGRkYmEwMDM3NDNiYzBkIiwiYXVkIjoiY2FzdGluZyBwcm9qZWN0IiwiaWF0IjoxNTk2MTQwNjkzLCJleHAiOjE1OTYyMjcwOTMsImF6cCI6IklLR1BWaVZQWXE1RTJjNlhXaGNUaTVKOU5iVUhSRVBnIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.I2s6ni-f6ZeMYIHyfwYUzA63bnyItDvTDuhRYBBcyuRaBiHNFvgDkcOWRYA-jE1uITx7ae1EzOSfC8UHwC8CDgibZHZojl6hFvalAom7D_FEFZtJtfOjyYkJbmkyG-Nf7CK6EwAoKkJSp_HLoVRJTM23NzGxaidfy0mznLuuD0lvR1TTsCLhKR_Xju1ae53t0X7fpGhpmJLFZC6639_OZxy5EugWxyfiELzYfWWEn5PaLdStzFQb_68wT-rerlxX__sT0mmMHI6-5mV7hxXmoEXZ8qBb28NHo8pj3vcan_HqIjRxF1CRr-9Arfgpi6tK9DMneoPfqMacN_GUgxt1cw"
}

director_headers = {
    "Authorization": "Bearer" + "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhUNW9JNF83elRmUndCRVBIa2FnaSJ9.eyJpc3MiOiJodHRwczovL3dlbmthaXRhbi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxZjYyY2NiYmQ4Y2UwMDNkNjIwNWY0IiwiYXVkIjoiY2FzdGluZyBwcm9qZWN0IiwiaWF0IjoxNTk2MTQwNjQxLCJleHAiOjE1OTYyMjcwNDEsImF6cCI6IklLR1BWaVZQWXE1RTJjNlhXaGNUaTVKOU5iVUhSRVBnIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.lEoUPAtpiSeXdpyrqE2rt4Xf2PONpM_lobUtHvcBY_Y-KDYhOyUAlEpjq0NFweTi0LooWjmnMuO3hsB819xwycTvKC9V6y0kJEQWELClj1O3C6Jqf4chHICvY8t8CTuxEpJiiI3Cr2pbnl5tjOtYi4EOI02ueGmgNuB0sTlbn3BLDqIH8iNwrvDHfNj1fw3nVQgo2pYLx_4mDVcF4gskI05QUD9BjoX8-O_mFZf83HNDEsRwq264fmapzbIXgTFZ6dcKlT2xXWvUDJsn9y4gfDawg0b2_G6rkzf--mGhZsEeldw9-JG4_tXiGei5v5Mun2fQJrlXuYsp6ri4ASCBFQ"
}

assistant_headers = {
    "Authorization": "Bearer" + "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhUNW9JNF83elRmUndCRVBIa2FnaSJ9.eyJpc3MiOiJodHRwczovL3dlbmthaXRhbi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxZjYyODYyOGRkYmEwMDM3NDNiYzBiIiwiYXVkIjoiY2FzdGluZyBwcm9qZWN0IiwiaWF0IjoxNTk2MTQwNTYwLCJleHAiOjE1OTYyMjY5NjAsImF6cCI6IklLR1BWaVZQWXE1RTJjNlhXaGNUaTVKOU5iVUhSRVBnIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.e6DMfDhqwv-U40l0qXcSlS1nS_6RT0ddgw8yj8-ZONxqIW78ZllmFTbTItAeK_WJbBi6ifq6MC3kOalruSlHMypr-VK1fSAA3FiTaiYKog0l9iXr5dvW_NVU0Xrvp-BdaQm5XqnC1BmQhxzLBOUxyaA_Btg3lrsdHsWQSNOqNEJAglp442ufRbkVwuozasxJS6LSq1OwgLwzsaV5McSmkKZFpTeXAD2A-KzB72YwK1f0-Edu9YnBZ4f6THeqBy3eqFYbXUKub007w1bOXWjjmk3sQGRHRPP09YgbXmq9jlraQWOnnQUeupQBM8BzV19hWCju43ty5xCnGbK0qZliRg"
}

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_project_test"
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

    def test_get_movies(self):
        res = self.client().get('/movies', headers=assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_movies_fail(self):
        res = self.client().get('movies', headers=assistant_headers)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    
    def test_get_actors(self):
        res = self.client().get('/actors', headers=assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_actors_fail(self):
        res = self.client().get('/actors', headers=assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_post_movies(self):
        new_movie = {
            "title":"test_movie",
            "release_date":"2020-07-29"
        }
        total_movies_before
        res = self.client().post('/movies', json=new_movie, headers=director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual()
    def test
