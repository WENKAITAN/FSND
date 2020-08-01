import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor,db
from auth import AuthError, requires_auth
import json

AUTH0_DOMAIN='wenkaitan.us.auth0.com'
ALGORITHMS=['RS256']
AUTH0_JWT_API_AUDIENCE='casting project'
AUTH0_CLIENT_ID='IKGPViVPYq5E2c6XWhcTi5J9NbUHREPg'
AUTH0_CALLBACK_URL='http://localhost:8080'
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  CORS(app)
  @app.after_request
  def after_request(response):
    response.headers.add("Access-Control-Allow-Methods",'GET, PUT, POST, DELETE, OPTIONS,')
    response.headers.add("Access-Control-Allow-Headers","Content-Type,Authorization, True")

    return response

  @app.route('/')
  def welcome():
    return jsonify("welcome to my app")

  @app.route("/authorization/url", methods=["GET"])
  def generate_auth_url():
      print(os.environ)
      url = f'https://{AUTH0_DOMAIN}/authorize' \
          f'?audience={AUTH0_JWT_API_AUDIENCE}' \
          f'&response_type=token&client_id=' \
          f'{AUTH0_CLIENT_ID}&redirect_uri=' \
          f'{AUTH0_CALLBACK_URL}'
      return jsonify({
          'url': url
      })
    
  '''
  APIS for actor
  '''
  
  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors(token):
    """
    This API fetches all actors with a short description
    Return the actors arrar or the arror handler
    """
    try:
      return jsonify({
        "success": True,
        "actors": [actor.format() for actor in Actor.query.all()]
      }), 200
    except:
      return jsonify({
        "success": False,
        "error": "An error occured"
      }), 500
  
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def add_actors(token):
    """
    This API creates a new actor
    Return the created actor info or the error handler
    """
    data = request.get_json()
    actor = Actor(
        name = data.get('name'),
        age = data.get('age'),
        gender = data.get('gender')
    )
    try:
      Actor.insert(actor)
      return jsonify({
        "success": True,
        "created": actor.id,
        "new_actor": actor.format()
      }), 200
    except:
      return jsonify({
        "success": False,
        "error": "An error occured"
      }), 500

  @app.route('/actors/<int:id>', methods=["PATCH"])
  @requires_auth('patch:actors')
  def update_actor(token,id):
    '''
    This API updates the actor info based on the id passes in from the parameter
    Return the deleted actor id or error handler
    '''
    data = request.get_json()
    actor = Actor.query.filter(Actor.id == id).one_or_none()
    try:

      if actor:
        actor.name = data.get('name') if 'name' in data else actor.name
        actor.age = data.get('age') if 'age' in data else actor.age
        actor.gender = data.get('gender') if 'gender' in data else actor.gender
        actor.update()

        return jsonify({
          "success": True,
          "updated":id,
          "updated_actor": actor.format()
        }),200
      else:
        abort(404)
    except:
      return jsonify({
        "success": False,
        "error": "An error occured"
      }), 500

  @app.route('/actors/<int:id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(token,id):
    '''
    This API deletes an actor based on the id from the parameter
    Return the deleted actor's id or error handler
    '''
    actor = Actor.query.get(id)
    try:
      if actor:
        actor.delete()
        return jsonify({
          "success": True,
          "actor": id
        }), 200
      else:
        abort(404)

    except:
      return jsonify({
        "success": False,
        "error": "An error occured"
      }),500

  '''
  APIS for movies
  '''
  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies(token):
    '''
    This API fetches all the movies
    Return the movie in an array or error handler
    '''
    try:
      return jsonify({
        "success": True,
        "movies": [movie.format() for movie in Movie.query.all()]
      }), 200
    except:
      return jsonify({
        "success": False,
        "error": "An error occured"
      }),500
  
  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def create_movie(token):
    '''
    This API creates a new movie
    Return the new created movie info or error handler
    '''
    data = request.get_json()

    title = data['title']
    release_date = data['release_date']
    try:
      movie = Movie(
        title=title,
        release_date=release_date
      )
      Movie.insert(movie)
      
      return jsonify({
        "success": True,
        "created": movie.id,
        "new_movie": movie.format()
      })
    except:
      return jsonify({
        "success":False,
        "error": "An error occured"
      }), 500

  @app.route('/movies/<id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_moive(token,id):
    '''
    This API updates the movie based on the id 
    Return the movies in array or error handler
    '''
    data = request.get_json()
    try:
      movie = Movie.query.filter(Movie.id == id).one_or_none()
      if movie:
        movie.title = data.get('title') if 'title' in data else movie.title
        movie.release_date = data.get('release_date') if 'release_date' in data else movie.release_date

        movie.update()
        return jsonify({
          "success": True,
          "updated": id,
          "updated_movie": movie.format()
        }), 200
      else:
        return jsonify({
          "success": False,
          "error": f"movie{id} not found."
        }), 404
    except:
      return jsonify({
        "success":False,
        "error":"an error occured"
      }), 500

  @app.route('/movies/<id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(token,id):
    '''
    This API deletes a movie based on the id passed in from the parameter
    Return the deleted movie id or error handler
    '''
    try:
      movie = Movie.query.filter(Movie.id == id).one_or_none()
      if movie:
        movie.delete()
        return jsonify({
          "success": True,
          "deleted": id
        }),200
      else:
        return jsonify({
          "success": False,
          "error": f"mvoie {id} not found"
        }), 404
    except:
      return jsonify({
        "success": False,
        "error": "An error occured"
      }), 500


  '''
  @implement error handler for Not Found
  '''
  @app.errorhandler(404)
  def notfound(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "not found"
    }), 404
  
  @app.errorhandler(500)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "unprocessable"
    }), 500

  '''
  @implement error handler for AuthError - DONE 
  '''
  @app.errorhandler(AuthError)
  def handle_auth_error(ex):
      """
      Receive the raised authorization error and propagates it as response
      """
      response = jsonify(ex.error)
      response.status_code = ex.status_code
      return response


  return app

 
