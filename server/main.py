import json
import requests
import pandas as pd
import pickle
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

MOVIE_METADATA = pd.read_csv('../data/movies_metadata.csv', low_memory=False)

origins = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/movie_list")
def get_movie_list():
    return MOVIE_METADATA.to_json()


@app.get("/api/{movie_id}")
def get_movie_metadata(movie_id: str):
    api_key = "400d81d9"
    # https://www.omdbapi.com/?i=tt0114709&apikey=400d81d9
    response = requests.get(
        f"https://www.omdbapi.com/?i={movie_id}&apikey={api_key}"
    )
    if response.status_code != 200:
        return {"alo": "Failed"}

    #
    # print(movie_ids)
    return json.loads(response.content.decode('utf-8'))


if __name__ == "__main__":
    config = uvicorn.Config("main:app", port=5000,
                            log_level="info", reload=True)
    server = uvicorn.Server(config)
    server.run()
