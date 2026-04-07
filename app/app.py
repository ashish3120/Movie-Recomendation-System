import streamlit as st
import pickle
import pandas as pd
import numpy as np


# custom loader to bypass numpy internal path issue
class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == "numpy._core.numeric":
            module = "numpy.core.numeric"
        return super().find_class(module, name)


def load_pickle(file_path):
    with open(file_path, "rb") as f:
        return CustomUnpickler(f).load()


# load files
movies_dict = load_pickle("../model/movie_list.pkl")
movies = pd.DataFrame(movies_dict)

similarity = load_pickle("../model/similarity.pkl")


# recommendation function
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[
        1:6
    ]

    recommended_movies = []

    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies


# UI
st.title("Movie Recommender System")

selected_movie_name = st.selectbox("Select a movie", movies["title"].values)

if st.button("Recommend"):
    recommendations = recommend(selected_movie_name)

    for movie in recommendations:
        st.write(movie)
