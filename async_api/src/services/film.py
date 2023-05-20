from functools import lru_cache

# import requests
# from api.v1.dependencies import (END_OF_FILM_LIST_TEXT,
#                                 GET_FILM_RESPONSE_ERROR_TEXT)
# from api.v1.deserializers.alice_deserializer import Intents
from core.config import film_settings
from db.base import BaseCache, BaseDB
from db.elastic import get_films_elastic
from db.redis import get_redis
from fastapi import Depends
from models.film import FilmModel
from services.base import BaseService


# from urllib.parse import urljoin, urlencode


class FilmService(BaseService):
    pass


@lru_cache()
def get_film_service(
        cache: BaseCache = Depends(get_redis),
        elastic: BaseDB = Depends(get_films_elastic),
) -> FilmService:
    return FilmService(
        index=film_settings.es_index,
        model=FilmModel,
        elastic=elastic,
        cache=cache,
    )

# async def film_list(page_size, page_number):
#    base_url = settings.base_url
#    params = {
#        "page[size]": page_size,
#        "page[number]": page_number if page_number != 999 else page_number-100
#    }
#    query_string = urlencode(params)
#    endpoint = urljoin(base_url, f"?{query_string}")
#    try:
#        with requests.get(endpoint) as response:
#            response.raise_for_status()
#            try:
#                films_model = FilmModel(**response.json()[0])
#            except ValueError:
#                return GET_FILM_RESPONSE_ERROR_TEXT, None
#            else:
#                response_text = f"Советую фильм: {films_model.title}, " \
#                                f"Рейтинг IMDB: {films_model.imdb_rating}, " \
#                                f"Жанр: {', '.join(films_model.genre)}"
#
#                return response_text, films_model.id
#
#    except requests.exceptions.RequestException as e:
#        return GET_FILM_RESPONSE_ERROR_TEXT
#
# def do_request(endpoint):
#    with requests.get(endpoint) as response:
#        response.raise_for_status()
#        films = response.json()
#
#    return films
#
# async def get_film_description(intents: Intents = None, state: dict = None) -> str:
#    base_url = settings.base_url + 'search'
#    params = {
#        "page[size]": 1,
#        "page[number]": 1,
#    }
#
#    if intents is not None:
#        film = intents.slots['Film'].value
#
#        params["query"] = film
#
#        endpoint = urljoin(base_url, f"?{urlencode(params)}")
#
#        try:
#            films = do_request(endpoint)
#
#            if len(films) == 0:
#                return f'Не нашла у себя фильм по запросу "{film}".'
#
#            uuid = films[0]['id']
#            endpoint = urljoin(base_url, f"{uuid}")
#
#            film_model = FilmModel(**do_request(endpoint))
#
#            title = film_model.title
#            description = film_model.description or 'Описание отсутствует'
#            response_text = f'Подробнее о фильме по запросу "{film}": Название: {title}, Описание: {description}'
#            return response_text
#
#        except requests.exceptions.RequestException:
#            return GET_FILM_RESPONSE_ERROR_TEXT
#
#    if state is not None:
#        uuid = state.get('id')
#        endpoint = urljoin(base_url, f"{uuid}")
#
#        try:
#            film_model = FilmModel(**do_request(endpoint))
#            title = film_model.title
#            description = film_model.description or 'Описание отсутствует'
#            response_text = f'Название: {title}, Описание: {description}'
#            return response_text
#
#        except requests.exceptions.RequestException as e:
#            print(e)
#            return GET_FILM_RESPONSE_ERROR_TEXT
