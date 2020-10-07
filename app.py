import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# import setup_db function from models to initialize Postgres database
from models import setup_db, Actors, Movies, db

from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    # call the setup_db() function from model.py to setup the POSTgres database
    setup_db(app)
    CORS(app)

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):

        actors = Actors.query.order_by(Actors.id).all()

        # print(actors)

        actors_formatted = [actor.format() for actor in actors]

        # print(actors_formatted)

        return jsonify({
            'success': True,
            'actors': actors_formatted
        })

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):

        movies = Movies.query.order_by(Movies.id).all()

        # print(movies)

        movies_formatted = [movie.format() for movie in movies]

        # print(movies_formatted)

        return jsonify({
            'success': True,
            'movies': movies_formatted
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(payload):
        body = request.get_json()

        actor_name = body.get('name', None)
        actor_age = body.get('age', None)
        actor_gender = body.get('gender', None)

        if not actor_name:
            abort(422, {'message': 'Name of actor not provided'})

        if not actor_age:
            abort(422, {'message': 'Age of actor not provided'})

        if not actor_gender:
            abort(422, {'message': 'Gender of actor not provided'})

        try:
            actor = Actors(name=actor_name, age=actor_age, gender=actor_gender)

            actor.insert()

            actors = Actors.query.order_by(Actors.id).all()
            total_actors = len(actors)
            last_actor = actors[total_actors - 1].format()
            # actors_formatted = [actor.format() for actor in actors]

            return jsonify({
                'success': True,
                'actor_added': last_actor
            })

        except BaseException:
            db.session.rollback()
            print(sys.exc_info())
            abort(422, {'message': 'Failed to add new actor to the database'})

        finally:
            db.session.close()

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(payload):
        body = request.get_json()

        movie_title = body.get('title', None)
        movie_release_date = body.get('release_date', None)

        if not movie_title:
            abort(422, {'message': 'Title of movie not provided'})

        if not movie_release_date:
            abort(422, {'message': 'Release date of movie not provided'})

        try:
            movie = Movies(title=movie_title, release_date=movie_release_date)

            movie.insert()

            movies = Movies.query.order_by(Movies.id).all()
            total_movies = len(movies)
            last_movie = movies[total_movies - 1].format()
            # movies_formatted = [movie.format() for movie in movies]

            return jsonify({
                'success': True,
                'movie_added': last_movie
            })

        except BaseException:
            db.session.rollback()
            print(sys.exc_info())
            abort(422, {'message': 'Failed to add new movie to the database'})
        finally:
            db.session.close()

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('update:actors')
    def update_actors(payload, id):

        actor = Actors.query.get(id)

        if actor is None:
            abort(
                404, {
                    'message': 'Actor ID requested not found in the database'})

        data = request.get_json()

        try:
            if 'name' in data:
                actor.name = data['name']

            if 'age' in data:
                actor.age = data['age']

            if 'gender' in data:
                actor.gender = data['gender']

            actor.update()

            return jsonify({
                'success': True,
                'actor': actor.format()
            })
        except BaseException:
            db.session.rollback()
            print(sys.exc_info())
            abort(
                422, {
                    'message': 'Failed to make updates to Actors database'})
        finally:
            db.session.close()

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('update:movies')
    def update_movies(payload, id):

        movie = Movies.query.get(id)

        if movie is None:
            abort(
                404, {
                    'message': 'Movie ID requested not found in the database'})

        data = request.get_json()

        try:
            if 'title' in data:
                movie.title = data['title']

            if 'release_date' in data:
                movie.release_date = data['release_date']

            movie.update()

            return jsonify({
                'success': True,
                'movie': movie.format()
            })
        except BaseException:
            db.session.rollback()
            print(sys.exc_info())
            abort(
                422, {
                    'message': 'Failed to make updates to movie in the database'})
        finally:
            db.session.close()

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, id):
        actor = Actors.query.get(id)

        if actor is None:
            abort(
                404, {
                    'message': 'Actor ID requested not found in the database'})

        try:

            actor.delete()

            return jsonify({
                'success': True,
                'deleted_actor': actor.format()
            })

        except BaseException:
            db.session.rollback()
            print(sys.exc_info())
            abort(422, {'message': 'Failed to delete the actor from database'})
        finally:
            db.session.close()

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, id):
        movie = Movies.query.get(id)

        if movie is None:
            abort(
                404, {
                    'message': 'Movie ID requested not found in the database'})

        try:

            movie.delete()

            return jsonify({
                'success': True,
                'deleted_movie': movie.format()
            })

        except BaseException:
            db.session.rollback()
            print(sys.exc_info())
            abort(422, {'message': 'Failed to delete the movie from database'})
        finally:
            db.session.close()

    # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": error_message(error, "Unprocessable")
        }), 422

    def error_message(error, default_text):

        try:
            # Return message contained in error, if possible
            return error.description['message']
        except BaseException:
            # otherwise, return given default text
            return default_text

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": error_message(error, "resource not found")
        }), 404

    @app.errorhandler(AuthError)
    def process_AuthError(AuthError):
        return jsonify({
            "success": False,
            "error": AuthError.status_code,
            "message": AuthError.error['description']
        }), AuthError.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
