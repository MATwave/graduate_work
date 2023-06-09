from uuid import UUID

from pydantic import BaseModel
from loguru import logger


class Person(BaseModel):
    id: UUID
    name: str


class FilmWork(BaseModel):
    id: UUID
    imdb_rating: float | None = 0.0
    genre: list[str]
    title: str
    description: str | None
    director: list[str]
    actors_names: list[str]
    writers_names: list[str]
    actors: list[Person]
    writers: list[Person]


class FilmTransformer:
    def __init__(self, data: list[list]) -> None:
        self.data = data

    def transform_data(self) -> list[dict]:
        if self.data:
            for films in self.data:
                films_batch = []
                for film in films:
                    grouped_data = self.group_data(film)
                    validated_data = self.validate_data(film, grouped_data)
                    films_batch.append(validated_data)
                yield films_batch

    def group_data(self, film: list):
        grouped = {
            'actors': [Person(id=person['person_id'], name=person['person_name']) for person in film[7] if
                       person['person_role'] == 'actor'],
            'writers': [Person(id=person['person_id'], name=person['person_name']) for person in film[7] if
                        person['person_role'] == 'writer'],
            'director': [person['person_name'] for person in film[7] if person['person_role'] == 'director']
        }
        actors_names = [person.name for person in grouped['actors']]
        writers_names = [person.name for person in grouped['writers']]
        grouped['actors_names'] = actors_names
        grouped['writers_names'] = writers_names
        return grouped

    def validate_data(self, film: list, data: dict) -> dict:
        try:
            film_work = FilmWork(
                id=film[0],
                imdb_rating=film[3],
                genre=film[8],
                title=film[1],
                description=film[2],
                director=data['director'],
                actors_names=data['actors_names'],
                writers_names=data['writers_names'],
                actors=data['actors'],
                writers=data['writers'],
            )
            return film_work.dict()
        except ValueError as e:
            logger.error(e)
