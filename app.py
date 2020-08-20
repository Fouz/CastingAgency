
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

from models import setup_db, Actor, Movie, db

from auth import AuthError, requires_auth


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

  @app.route("/")
  def home():
    return jsonify({
        "success":True,
        "message": "Hello from the other side"
    })
  #   GET movies and actors 
  @app.route("/movies", methods=['GET'])
  def movies():
    movies = Movie.query.all()
    movies_dict = {mov.id: mov.type for mov in movies}
    if len(movies) == 0:
      return jsonify({
        'success':False,
        "messages": "there're no movies at the moment come on another time"
      })
      return jsonify({
          "success": True,
          "total_movies": len(movies_dict),
          "movies": movies_dict,
      })

  @app.route("/movies/<int:id>", methods=['GET'])
  def movie(id):
    current = db.session.query(Movie).get(id)
    if current is None :
          return jsonify({
              "success": False,
              "message": "ther's no such movie!!!!!!",
          })
          
    return jsonify({
        "success": True,
        "movie": current,
    })

  @app.route("/actors", methods=['GET'])
  def actors():
    actors = Actor.query.all()
    actors_dict = {act.id: act.type for act in actors}
    if len(actors) == 0:
      return jsonify({
          'success': False,
          "messages": "all actors swallowed by the black hole."
      })
    return jsonify({
        "success": True,
        "total_actors": len(actors_dict),
        "actors": actors_dict,
    })


  @app.route("/actors/<int:id>", methods=['GET'])
  def actor(id):
    current = db.session.query(Actor).get(id)
    if current is None:
          return jsonify({
              "success": False,
              "message": "the actor you're looking for does not exist!",
          })
    return jsonify({
        "success": True,
        "actor": current,
    })

  #  POST movies and actors

  @app.route("/movies/new", methods=['POST'])
  @requires_auth('post:movie')
  def movies_new(jwt):
    form = request.form
    title = form.get('title')
    release_date = form.get('release date')
    actors = form.get('actors')
    try:
      movie = Movie(movie_title=title, answer=answer, release_date=release_date, actors=actors)
      movie.insert()
    except:
      db.session.rollback()
    finally:
      db.session.close()
    return jsonify({
        "success": True,
        "message": "movie created"
      })

  @app.route("/actors/new", methods=['POST'])
  @requires_auth('post:actor')
  def actors_new(jwt):
    form = request.form
    name = form.get('name')
    age = form.get('age')
    gender = form.get('gender')
    movies = form.get('movies')
    try:
      actor = Actor(name=name, age=age, gender=gender, movies=movies)
      movie.insert()
    except:
      db.session.rollback()
    finally:
      db.session.close()
    return jsonify({
        "success": True,
        "message": "actor created"
      })

  #  DELETE movies and actors

  @app.route("/movies/<int:id>", methods=['DELETE'])
  @requires_auth('delete:movie')
  def movie_delete(jwt,id):
    movie = db.session.query(Movie).get(id).first_or_404()
    try:
      movie.delete()
    except:
      db.session.rollback()
    finally:
      db.session.close()
    return jsonify({
      "success":True,
      "message": "bye bye, movie deleted"
    })

  @app.route("/actors/<int:id>", methods=['DELETE'])
  @requires_auth('delete:actor')
  def actor_delete(jwt,id):
    actor = db.session.query(Actor).get(id).first_or_404()
    try:
      actor.delete()
    except:
      db.session.rollback()
    finally:
      db.session.close()
    return jsonify({
      "success":True,
      "message": "deleted"
    })

  #  PATCH movies and actors

  @app.route("/actors/<int:id>/patch", methods=['POST'])
  @requires_auth('patch:actor')
  def actor_patch(jwt,id):
    current = db.session.query(Actor).get(id)
    form = request.form
    # if not ('name' in form and 'age' in form and 'gender' in form and 'movies' in form):
    #   abort(422)
    name = form.get('name')
    age = form.get('age')
    gender = form.get('gender')
    movies = form.get('movies')
    try:
      current.name = name
      current.age = age
      current.gender = gender
      current.movies = movies
      current.insert()
    except:
      db.session.rollback()
    finally:
      db.session.close()
    return jsonify({
        "success": True,
        "message": "actor editied"

      })

  @app.route("/movies/<int:id>/patch", methods=['POST'])
  @requires_auth('patch:movie')
  def movie_patch(jwt,id):
    current = db.session.query(Movie).get(id)
    form = request.form
    # if not ('title' in form and 'release date' in form and 'actors' in form):
    #   abort(422)
    title = form.get('title')
    release_date = form.get('release date')
    actors = form.get('actors')
    try:
      current.movie_title = title
      current.release_date = release_date
      current.actors = actors
      current.insert()
    except:
      db.session.rollback()
    finally:
      db.session.close()
    return jsonify({
        "success": True,
        "message": "movie editied"

      })

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success":False,
      "error":404,
      "message": "resource not found"
      }),404
  
  @app.errorhandler(405)
  def not_allowed(error):
      return jsonify({
          "success": False,
          "error": 405,
          "message": "Method not allowed"
      }), 405
  
  @app.errorhandler(422)
  def not_found(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(AuthError)
    def invalid_claims(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": error.__dict__
        }), 401
  
  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
