from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from services.film import FilmService, get_film_service

from .dependencies import FILM_DETAILS_MESSAGE, FilmFilterParams, FilmQueryParams
from .serializers.movies_serializers import APIFilm, APIFilmFull

router = APIRouter()


@router.get("/search", response_model=list[APIFilm], summary="Поиск по фильмам")
async def film_search(commons: FilmQueryParams = Depends(FilmQueryParams),
                      film_service: FilmService = Depends(get_film_service),) -> list[APIFilm]:
    """
    Полнотекстовый поиск по фильмам
    """
    page = {"size": commons.size, "number": commons.number}
    query = {"field": "title", "value": commons.query}
    params = {"query": query, "page": page, "sort": commons.sort}
    films = await film_service.get(params)
    if films is None:
        return []
    return [APIFilm.parse_obj(film.dict(by_alias=True)) for film in films]


@router.get("/{film_id}", response_model=APIFilmFull, summary="Поиск фильма по UUID")
async def film_details(
    film_id: UUID, film_service: FilmService = Depends(get_film_service)
) -> APIFilmFull:
    """
    Полная информация по фильму по его UUID
    """
    film = await film_service.get(film_id)
    if not film:  # Если фильм не найден, отдаём 404 статус
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=FILM_DETAILS_MESSAGE)
    return APIFilmFull(**film.dict(by_alias=True))


@router.get("/", response_model=list[APIFilm], summary="Список фильмов с фильтрацией по жанру")
async def film_list(commons: FilmFilterParams = Depends(FilmFilterParams),
                    film_service: FilmService = Depends(get_film_service)) -> list[APIFilm]:
    """
    Вывод списка фильмов с возможностью фильтрации по жанру
    """
    page = {"size": commons.size, "number": commons.number}
    filter_parameter = {"field": "genre", "value": commons.genre}
    params = {"page": page, "filter_parameter": filter_parameter, "sort": commons.sort}
    films = await film_service.get(params)
    if films is None:  # Если фильмы не найден, отдаём пустой список
        return []
    return [APIFilm.parse_obj(film.dict(by_alias=True)) for film in films]
