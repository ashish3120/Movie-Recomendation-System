# import streamlit as st
# import pickle
# import pandas as pd


# # -------------------------
# # custom loader
# # -------------------------
# class CustomUnpickler(pickle.Unpickler):
#     def find_class(self, module, name):
#         if module == "numpy._core.numeric":
#             module = "numpy.core.numeric"
#         return super().find_class(module, name)


# def load_pickle(file_path):
#     with open(file_path, "rb") as f:
#         return CustomUnpickler(f).load()


# # -------------------------
# # CACHE LOADING (IMPORTANT)
# # -------------------------
# @st.cache_resource
# def load_data():

#     movies_dict = load_pickle("../model/movie_list.pkl")
#     similarity = load_pickle("../model/similarity.pkl")

#     movies = pd.DataFrame(movies_dict)

#     return movies, similarity


# movies, similarity = load_data()


# # -------------------------
# # recommend function
# # -------------------------
# def recommend(movie):

#     movie_index = movies[movies["title"] == movie].index[0]

#     distances = similarity[movie_index]

#     movies_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[
#         1:6
#     ]

#     recommended_movies = []

#     for i in movies_list:
#         recommended_movies.append(movies.iloc[i[0]].title)

#     return recommended_movies


# # -------------------------
# # UI
# # -------------------------
# st.title("Movie Recommender System")

# selected_movie_name = st.selectbox("Select a movie", movies["title"].values)

# if st.button("Recommend"):
#     recommendations = recommend(selected_movie_name)

#     for movie in recommendations:
#         st.write(movie)


# imports
import streamlit as st
import pickle
import pandas as pd
import os
import requests


# -------------------------
# download links
# -------------------------

SIMILARITY_URL = (
    "https://huggingface.co/datasets/ashish3120/movies/resolve/main/similarity.pkl"
)
MOVIE_LIST_URL = (
    "https://huggingface.co/datasets/ashish3120/movies/resolve/main/movie_list.pkl"
)

SIMILARITY_PATH = "similarity.pkl"
MOVIE_LIST_PATH = "movie_list.pkl"


# -------------------------
# download function
# -------------------------


def download_file(url, path):

    if os.path.exists(path):
        return

    st.write("Downloading:", path)

    r = requests.get(url, stream=True)

    with open(path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)


# -------------------------
# pickle loader
# -------------------------


class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):

        if module == "numpy._core.numeric":
            module = "numpy.core.numeric"

        return super().find_class(module, name)


# -------------------------
# load data
# -------------------------


@st.cache_resource
def load_data():

    download_file(SIMILARITY_URL, SIMILARITY_PATH)

    download_file(MOVIE_LIST_URL, MOVIE_LIST_PATH)

    with open(MOVIE_LIST_PATH, "rb") as f:
        movies_dict = CustomUnpickler(f).load()

    with open(SIMILARITY_PATH, "rb") as f:
        similarity = CustomUnpickler(f).load()

    movies = pd.DataFrame(movies_dict)

    return movies, similarity


st.title("Movie Recommender System")

# st.write("Loading data...")

movies, similarity = load_data()

st.success("Model loaded successfully")


# -------------------------
# recommend function
# -------------------------


def recommend(movie):

    movie_index = movies[movies["title"] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[
        1:6
    ]

    recommended_movies = []

    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies


# -------------------------
# UI
# -------------------------

selected_movie_name = st.selectbox("Select a movie", movies["title"].values)

if st.button("Recommend"):
    recommendations = recommend(selected_movie_name)

    for movie in recommendations:
        st.write(movie)
