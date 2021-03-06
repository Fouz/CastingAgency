import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref

import json

database_path = "postgres+psycopg2://baftfehglspnqq:473bde560480bb01105756fbf4e19a634897bee74ec326f4a485d54b4bcbfda6@ec2-54-224-124-241.compute-1.amazonaws.com: 5432/d4dl7bdg09o6l5"
# postgres: // baftfehglspnqq: 473bde560480bb01105756fbf4e19a634897bee74ec326f4a485d54b4bcbfda6@ec2-54-224-124-241.compute-1.amazonaws.com: 5432/d4dl7bdg09o6l5


db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


# class Movies_Actors(db.Model):
#     __tablename__ = 'movies_actors'
#     id = db.Column(db.Integer, primary_key=True)
#     movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
#     actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'))

#     movie = relationship(Movie, backref=backref("movies_actors", cascade="all, delete-orphan"))
#     actor = relationship(Actor, backref=backref("movies_actors", cascade="all, delete-orphan"))

# movies_actors = db.Table("movies_actors",
#     Column('id', Integer, primary_key=True),
#     Column("actor_id", db.Integer, db.ForeignKey("actor.actor_id")),
#     Column("movie_id", db.Integer, db.ForeignKey("movie.movie_id"))
# )

class Movie(db.Model):  
    __tablename__ = "movie"
    movie_id = Column(Integer, primary_key=True)
    movie_title = Column(String)
    release_date = Column(String)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'movie_title': self.movie_title,
            'release_date': self.release_date,
        }

class Actor(db.Model):  
    __tablename__ = "actor"
    actor_id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }
