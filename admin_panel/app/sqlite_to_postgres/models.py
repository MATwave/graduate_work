from dataclasses import dataclass


@dataclass
class FilmWork:
    id: str
    title: str
    type: str
    created: str
    modified: str
    creation_date: str | None = None
    file_path: str | None = None
    description: str | None = None
    rating: float | None = None


@dataclass
class Genre:
    id: str
    name: str
    created: str
    modified: str
    description: str | None = None


@dataclass
class Person:
    id: str
    full_name: str
    created: str
    modified: str


@dataclass
class GenreFilmWork:
    id: str
    genre_id: str
    film_work_id: str
    created: str


@dataclass
class PersonFilmWork:
    id: str
    film_work_id: str
    person_id: str
    role: str
    created: str
