import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actors, Movies
# get jwt tokens from the config file to send http requests for
# authorization in test file.
from config import jwt_tokens
from sqlalchemy import desc
from datetime import date

# Setting up unit tests

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # See readme to setup test database using the supplied
        # capstone_test.psql file
        self.database_path = os.environ['TEST_DATABASE_URL']
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

# Unit Tests
# One test for success behavior of each endpoint
# At least two tests of RBAC for each role

# Below test checks "success" for "Get actors" endpoint and Tests for
# Casting Assistant RBAC Role (1st test)

    def test_get_actors(self):

        res = self.client().get(
            '/actors',
            headers={
                'Authorization': jwt_tokens['casting_assistant']})

        data = json.loads(res.data)
        print('\n Test - 1: Actors data from test database')
        print(data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

# Below test checks "success" for "Get Movies" endpoint and Tests for
# Casting Assistant RBAC Role (2nd test)

    def test_get_movies(self):

        res = self.client().get(
            '/movies',
            headers={
                'Authorization': jwt_tokens['casting_assistant']})

        data = json.loads(res.data)
        print('\n Test - 2: Movies data from test database')
        print(data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

# Below test checks "success" for "Post Actors" endpoint and Tests for
# "Casting Director" RBAC Role (1s test)

    def test_post_actors(self):

        new_actor = {
            "name": "Jeff",
            "age": 42,
            "gender": "male"
        }

        res = self.client().post(
            '/actors',
            json=new_actor,
            headers={
                'Authorization': jwt_tokens['casting_director']})

        data = json.loads(res.data)
        print('\n Test - 3: Data for new actor posted to test database')
        print(data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor_added']['name'], new_actor['name'])

# Below test checks "success" for "Post Movies" endpoint and Tests for
# "Executive Producer" RBAC Role (1st test)

    def test_post_movies(self):

        new_movie = {
            "title": "Dinos",
            "release_date": "2020-10-04"
        }

        res = self.client().post(
            '/movies',
            json=new_movie,
            headers={
                'Authorization': jwt_tokens['executive_producer']})

        data = json.loads(res.data)
        print('\n Test - 4: Data for new Movie posted to test database')
        print(data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie_added']['title'], new_movie['title'])

# Below test checks "success" for "Patch/update Actors" endpoint and Tests
# for "Casting Director" RBAC Role (2nd test)

    def test_patch_actors(self):

        update_actor = {
            "age": 21
        }

        res = self.client().patch(
            '/actors/1',
            json=update_actor,
            headers={
                'Authorization': jwt_tokens['casting_director']})

        data = json.loads(res.data)
        print('\n Test 5: Data for updating actor # 1 age from test database')
        print(data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['age'], update_actor['age'])

# Below test checks "success" for "Patch/update Movie" endpoint and Tests
# for "Executive Producer" RBAC Role (2nd test)

    def test_patch_movies(self):

        update_movie = {
            "title": "Panther"
        }

        res = self.client().patch(
            '/movies/1',
            json=update_movie,
            headers={
                'Authorization': jwt_tokens['executive_producer']})

        data = json.loads(res.data)
        print('\n Test 6: Data for updating Movie # 1 age from test database')
        print(data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['title'], update_movie['title'])

# Below test checks "success" for "Delete Actor" endpoint and Tests for "Casting Director" RBAC Role (3rd test)
# Delte actor # 2

    def test_delete_actor(self):

        res = self.client().delete('/actors/2',
                                   headers={'Authorization': jwt_tokens['casting_director']})

        data = json.loads(res.data)
        print('\n Test 7: Data for deleting actor # 2 from test database')
        print(data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

# Below test checks "success" for "Delete Movie" endpoint and Tests for "Executive Producer" RBAC Role (3rd test)
# Delte movie # 2

    def test_delete_movie(self):

        res = self.client().delete('/movies/2',
                                   headers={'Authorization': jwt_tokens['executive_producer']})

        data = json.loads(res.data)
        print('\n Test 8: Data for deleting movie # 2 from test database')
        print(data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

# Testing for error behavior of each endpoint
# -------------------------------------------

# Below test checks AuthError for "Get actors" endpoint. Expired bearer token

    def test_AuthError_401_get_actors(self):

        res = self.client().get(
            '/actors',
            headers={
                'Authorization': jwt_tokens['expired_token']})

        data = json.loads(res.data)
        print('\n Test 9: AuthError data from server')
        print(data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

# Below test checks AuthError for "Get movies" endpoint. Expired bearer token

    def test_AuthError_401_get_movies(self):

        res = self.client().get(
            '/movies',
            headers={
                'Authorization': jwt_tokens['expired_token']})

        data = json.loads(res.data)
        print('\n Test 10: AuthError data from server')
        print(data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

# Below test checks "error - bad data sent to endpoint" for "Post Actors"
# endpoint

    def test_error_422_post_actors(self):

        new_actor = {
            "age": 42,
            "gender": "male"
        }

        res = self.client().post(
            '/actors',
            json=new_actor,
            headers={
                'Authorization': jwt_tokens['casting_director']})

        data = json.loads(res.data)
        print('\n Test 11: Data for new actor posted to test database')
        print(data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Name of actor not provided")

# Below test checks "error - bad data sent to endpoint" for "Post Movies"
# endpoint

    def test_error_422_post_movies(self):

        new_movie = {
            "release_date": "2020-10-04"
        }

        res = self.client().post(
            '/movies',
            json=new_movie,
            headers={
                'Authorization': jwt_tokens['executive_producer']})

        data = json.loads(res.data)
        print('\n Test 12: Title of Movie not provided to Post endpoint')
        print(data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Title of movie not provided")

# Below test checks "AuthError - Invalid Permissions" for "Post Movies"
# endpoint

    def test_AuthError_401_post_movies(self):

        new_movie = {
            "title": "Dinos",
            "release_date": "2020-10-04"
        }

        res = self.client().post(
            '/movies',
            json=new_movie,
            headers={
                'Authorization': jwt_tokens['casting_director']})

        data = json.loads(res.data)
        print('\n Test 13: Invalid Auth0 permission sent to post Movies endpoint')
        print(data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Permission not found")

# Below test checks "error - Invalid actor id" for "Patch Actor" endpoint

    def test_error_404_patch_actor(self):

        new_actor = {
            "name": "Jeff",
            "age": 42,
            "gender": "male"
        }

        res = self.client().patch(
            '/actors/100',
            json=new_actor,
            headers={
                'Authorization': jwt_tokens['executive_producer']})

        data = json.loads(res.data)
        print('\n Test 14: Actor ID not found in the database')
        print(data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(
            data['message'],
            "Actor ID requested not found in the database")

# Below test checks "error - Invalid Movie id" for "Patch Movie" endpoint

    def test_error_404_patch_movie(self):

        update_movie = {
            "title": "Panther"
        }

        res = self.client().patch(
            '/movies/100',
            json=update_movie,
            headers={
                'Authorization': jwt_tokens['executive_producer']})

        data = json.loads(res.data)
        print('\n Test 15: Movie ID not found in the database')
        print(data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(
            data['message'],
            "Movie ID requested not found in the database")

# Below test checks "error - Invalid actor id" for "Delete Actor" endpoint

    def test_error_404_delete_actor(self):

        res = self.client().delete('/actors/100',
                                   headers={'Authorization': jwt_tokens['executive_producer']})

        data = json.loads(res.data)
        print('\n Test 16: Actor ID not found in the database')
        print(data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(
            data['message'],
            "Actor ID requested not found in the database")

# Below test checks "error - Invalid Movie id" for "Delete Movie" endpoint

    def test_error_404_delete_movie(self):

        res = self.client().delete('/movies/100',
                                   headers={'Authorization': jwt_tokens['executive_producer']})

        data = json.loads(res.data)
        print('\n Test 17: Movie ID not found in the database')
        print(data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(
            data['message'],
            "Movie ID requested not found in the database")

# Below test checks "AuthError - Invalid Permissions" for "Delete Actor"
# endpoint

    def test_error_401_delete_actor(self):

        res = self.client().delete('/actors/3',
                                   headers={'Authorization': jwt_tokens['casting_assistant']})

        data = json.loads(res.data)
        print('\n Test 18: Casting Assistant does not have permission to delete actor')
        print(data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Permission not found")

# Below test checks "AuthError - Invalid Permissions" for "Delete Movie"
# endpoint

    def test_error_401_delete_movie(self):

        res = self.client().delete('/movies/3',
                                   headers={'Authorization': jwt_tokens['casting_director']})

        data = json.loads(res.data)
        print('\n Test 19: Casting Director does not permission to delete movies')
        print(data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Permission not found")

# From app directory, run 'python test_app.py' to start tests

if __name__ == "__main__":
    unittest.main()