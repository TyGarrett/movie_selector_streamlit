import streamlit as st
from google.cloud import firestore

from util import add_user, add_movie, get_users, get_movies, delete_user, delete_movie, get_db

db = get_db()
users = get_users(db)
movies = get_movies(db)

with st.expander("Add User"):
    user_name = st.text_input("User Name")
    if st.button("Add", key="User"):
        add_user(db, user_name)

with st.expander("Delete User"):
    user_name = st.selectbox("User Name", [user.name for user in users])
    if st.button("Delete", key="User"):
        delete_user(db, user_name)

with st.expander("Add Movie"):
    movie_name = st.text_input("Movie Title")
    movie_users = st.multiselect("User", [user.name for user in users])
    if st.button("Add", key="Movie"):
        add_movie(db, movie_name, movie_users)

with st.expander("Delete Movie"):
    movie_title = st.selectbox("Movie Title", [movie.title for movie in movies])
    if st.button("Delete", key="Movie"):
        delete_movie(db, movie_title)

users = get_users(db)
movies = get_movies(db)

st.subheader("Users")
st.dataframe([user.to_dict() for user in users])
st.subheader("Movies")
st.dataframe([movie.to_dict() for movie in movies])
