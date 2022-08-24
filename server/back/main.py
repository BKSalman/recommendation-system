import pickle
from random import randint

import pandas as pd
import requests
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import EstimateRequest, EstimateResponse, Recommend
from utils import get_recommendations

app = FastAPI()

# https://www.omdbapi.com/?i=tt0114709&apikey=400d81d9
API_KEY = "400d81d9"

LOADED_MODEL = pickle.load(open("../../recommendation_model.sav", 'rb'))

MOVIE_METADATA = pd.read_csv(
    '../../data/movies_metadata.csv', low_memory=False)


MOVIE_RATINGS = pd.read_csv("../../data/ratings_small.csv")

MOVIE_METADATA = MOVIE_METADATA[MOVIE_METADATA["vote_count"] >= 55]

MOVIE_METADATA = MOVIE_METADATA.fillna('')

# IDs of movies with count more than 55
MOVIE_IDS = [int(x) for x in MOVIE_METADATA['id'].values]

# Select ratings of movies with more than 55 counts
MOVIE_RATINGS = MOVIE_RATINGS[MOVIE_RATINGS['movieId'].isin(MOVIE_IDS)]

# Reset Index
MOVIE_RATINGS.reset_index(inplace=True, drop=True)

MOVIE_METADATA = MOVIE_METADATA[["id", "imdb_id",
                                 "genres", "original_title", "title", "vote_count"]]
MOVIE_DICT = MOVIE_METADATA.to_dict(orient="index")


def is_rated(user_id: int, movie_id: int) -> bool:
    # creating a user item interactions matrix
    user_movie_interactions_matrix = MOVIE_RATINGS.pivot(
        index='userId', columns='movieId', values='rating')
    # extracting those product ids which the user.user_id has not interacted with yet
    not_rated_movies = user_movie_interactions_matrix.loc[user_id][user_movie_interactions_matrix.loc[user_id].isnull(
    )].index.tolist()

    if movie_id not in not_rated_movies:
        return True
    return False


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/user-list")
def get_users_list():
    users = MOVIE_RATINGS["userId"].drop_duplicates().to_list()
    return users


@app.get("/api/movie-list/{user_id}")
def get_movies_list(user_id: int):
    # creating a user item interactions matrix
    user_movie_interactions_matrix = MOVIE_RATINGS.pivot(
        index='userId', columns='movieId', values='rating')

    # extracting those product ids which the user_id has not interacted with yet
    non_rated_movies = user_movie_interactions_matrix.loc[user_id][
        user_movie_interactions_matrix.loc[user_id].isnull()].index.tolist()
    return non_rated_movies


@app.get("/api/poster/{movie_id}")
def get_movie_metadata(movie_id: str):
    movie = MOVIE_METADATA.loc[MOVIE_METADATA["id"] == movie_id]

    response = requests.get(
        f"https://www.omdbapi.com/?i={[loop_id for loop_id in movie['imdb_id']][0]}&apikey={API_KEY}"
    )
    if response.status_code == 404:
        return {"Message": "Not found"}

    return response.json()["Poster"]


@app.get("/api/recommend")
def get_recommendation(recommend: Recommend):
    top_recommendations = get_recommendations(MOVIE_RATINGS, MOVIE_METADATA,
                                              recommend.user_id, 10, LOADED_MODEL)

    return top_recommendations


@app.get("/api/estimate")
def estimate_rating(user_id: int, movie_id: int):
    if is_rated(user_id, movie_id):
        return {"Message": "movie already rated"}
    est: int = LOADED_MODEL.predict(
        user_id, movie_id).est

    return est


if __name__ == "__main__":
    config = uvicorn.Config("main:app", port=5000,
                            log_level="info", reload=True)
    server = uvicorn.Server(config)
    server.run()
