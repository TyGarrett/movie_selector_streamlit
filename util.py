from dataclasses import dataclass
import json

from google.oauth2 import service_account
from google.cloud import firestore
import streamlit as st


@dataclass
class Movie:
    title: str
    users: list

    def to_dict(self):
        return {'title': self.title, 'users': self.users}

    @staticmethod
    def from_dict(d):
        return Movie(d['title'], d['users'])

    def __str__(self):
        return self.title


@dataclass
class User:
    name: str

    def to_dict(self):
        return {'name': self.name}

    @staticmethod
    def from_dict(d):
        return User(d['name'])

    def __str__(self):
        return self.name


def add_movie(db, movie_name, movie_users):
    movie = Movie(movie_name, movie_users)
    db.collection("movies").add(movie.to_dict())


def add_user(db, user_name):
    user = User(user_name)
    db.collection("users").add(user.to_dict())


def get_users(db):
    posts_ref = db.collection("users")
    return [User.from_dict(doc.to_dict()) for doc in posts_ref.stream()]


def delete_user(db, user_name):
    posts_ref = db.collection("users")
    doc_ids = [doc.id for doc in posts_ref.stream() if doc.to_dict()['name'] == user_name]

    for doc_id in doc_ids:
        db.collection('movies').document(doc_id).delete()


def get_movies(db):
    posts_ref = db.collection("movies")
    return [Movie.from_dict(doc.to_dict()) for doc in posts_ref.stream()]


def delete_movie(db, movie_title):
    posts_ref = db.collection("movies")
    doc_ids = [doc.id for doc in posts_ref.stream() if doc.to_dict()['title'] == movie_title]

    for doc_id in doc_ids:
        db.collection('movies').document(doc_id).delete()


def get_db():
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project="movies-139fd")
    return db
