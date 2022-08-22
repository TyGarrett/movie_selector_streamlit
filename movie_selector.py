import random
import streamlit as st

from util import get_users, get_movies, get_db

db = get_db()

st.title("Movie Selector")
users = get_users(db)
movies = get_movies(db)

user1_tab, user2_tab = st.columns(2)
user1 = user1_tab.selectbox('First User', [user.name for user in users])
user2 = user2_tab.selectbox('Seconds User', [user.name for user in users if user.name != user1])

user1_weight = st.slider("User Selection Weight", min_value=0.0, max_value=1.0, value=0.5, step=0.05)
user2_weight = 1 - user1_weight

if st.button("Select Movie"):
    user1_movies = [movie for movie in movies if user1 in movie.users]
    user2_movies = [movie for movie in movies if user2 in movie.users]

    if random.random() < user1_weight:
        movie = random.choice(user1_movies)
    else:
        movie = random.choice(user2_movies)

    st.subheader(movie.title)
