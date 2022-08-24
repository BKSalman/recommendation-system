from pydantic import BaseModel


class Recommend(BaseModel):
    user_id: int


class EstimateRequest(BaseModel):
    user_id: int
    movie_id: int


class EstimateResponse(BaseModel):
    estimation: int
