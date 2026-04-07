import os
import pickle
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# -------------------------
# Custom Unpickler
# -------------------------
class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == "numpy._core.numeric":
            module = "numpy.core.numeric"
        return super().find_class(module, name)


def load_pickle(file_path):
    with open(file_path, "rb") as f:
        return CustomUnpickler(f).load()


# -------------------------
# Load model data at startup
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "model")

movies_dict = load_pickle(os.path.join(MODEL_DIR, "movie_list.pkl"))
similarity = load_pickle(os.path.join(MODEL_DIR, "similarity.pkl"))
movies = pd.DataFrame(movies_dict)

# -------------------------
# FastAPI app
# -------------------------
app = FastAPI(
    title="Movie Recommender API",
    description="Content-based movie recommendation engine using cosine similarity",
    version="1.0.0",
)

# Allow all origins for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# Schemas
# -------------------------
class RecommendRequest(BaseModel):
    movie: str


class RecommendResponse(BaseModel):
    movie: str
    recommendations: list[str]


# -------------------------
# Routes
# -------------------------
@app.get("/")
def root():
    return {"status": "ok", "message": "Movie Recommender API is running"}


@app.get("/api/movies")
def get_movies():
    """Return all available movie titles."""
    return {"movies": movies["title"].tolist()}


@app.post("/api/recommend", response_model=RecommendResponse)
def get_recommendations(request: RecommendRequest):
    """Return top 5 similar movies for a given movie title."""
    movie_title = request.movie

    matches = movies[movies["title"] == movie_title]
    if matches.empty:
        raise HTTPException(status_code=404, detail=f"Movie '{movie_title}' not found")

    movie_index = matches.index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)), key=lambda x: x[1], reverse=True
    )[1:6]

    recommended = [movies.iloc[i[0]].title for i in movies_list]

    return RecommendResponse(movie=movie_title, recommendations=recommended)


@app.get("/api/health")
def health():
    return {"status": "healthy", "total_movies": len(movies)}
