from uuid import UUID

import orjson
from models.base import orjson_dumps
from pydantic import BaseModel, validator


class BaseOrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class RoleAndFilms(BaseOrjsonModel):
    role: str
    film_ids: list[UUID]


class APIGenre(BaseOrjsonModel):
    id: UUID
    name: str
    description: str | None
    film_ids: list[UUID]


class APIPersonBase(BaseOrjsonModel):
    id: UUID
    name: str


class APIPerson(APIPersonBase):
    roles: list[RoleAndFilms]


class APIFilm(BaseOrjsonModel):
    id: UUID
    title: str
    imdb_rating: float
    genre: list[str]


class APIFilmFull(APIFilm):
    description: str | None
    actors: list[APIPersonBase] | None = []
    writers: list[APIPersonBase] | None = []
    directors: list[APIPersonBase] | None = []

    @validator('description', pre=True, always=True)
    def check_empty_decription(cls, description):
        if description:
            return description
        return 'Описание отсутствует'


class APIPersonFilms(BaseOrjsonModel):
    role: str
    films: list[APIFilm]
