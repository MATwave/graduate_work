from uuid import UUID

from src.models.base import BaseOrjsonModel


class Person(BaseOrjsonModel):
    id: UUID
    name: str


class FilmModel(BaseOrjsonModel):
    title: str
    imdb_rating: float | None = 0.0
    genre: list[str] = []
    description: str | None = ""
    director: list[str] | None = []
    actors_names: list[str] = []
    writers_names: list[str] = []
    actors: list[Person] | None = []
    writers: list[Person] | None = []


class RoleAndFilmsModel(BaseOrjsonModel):
    role: str
    films: list[FilmModel]
