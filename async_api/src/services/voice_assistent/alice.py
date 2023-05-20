import random
from functools import lru_cache
from urllib.parse import urljoin, urlencode

import aiohttp
from core.config import settings
from core.voice_command.comand import text_commands
from fastapi import status
from loguru import logger
from models.film import FilmModel
from models.voice_model.alice.request import AliceRequestModel
from models.voice_model.alice.response import AliceResponse, AliceResponseModel


class AliceService:

    async def get_data_assistant(self, alice_request_model: AliceRequestModel) -> AliceResponseModel:
        """Основной метод для ызаимодействия с голосовым ассистенотм."""

        response = AliceResponse(alice_request_model.dict())

        # Реакция на приветствие
        if alice_request_model.session.new:
            logger.info('определили новую сессию')
            response.set_text(text_commands.welcome)
            response.set_buttons(text_commands.end)
            return response.dumps()

        elif 'exit' in alice_request_model.request.nlu.intents:
            logger.info('определили интент exit')
            response.set_text(text_commands.bye)
            response.end()
            return response.dumps()

        # Реакция на просьбу показать фильм
        elif 'get_film' in alice_request_model.request.nlu.intents:
            logger.info('определили интент get_film')
            text, state = await self._recommendation_film(state=dict())
            response.set_text(text)
            response.set_state(state_dict={'get_film': state})
            return response.dumps()

    ## Ответ на вопросы по найденному фильму.
    # if state:
    #    resp.response.text = await self._context_answer_to_questions(command=requestMarusya.request.command,
    #                                                                 request=request,
    #                                                                 session_id=session_id,
    #                                                                 state=state)
    #    return dict(resp)

    # return dict(resp)

    async def _get_data_from_http(self, **kwargs):
        """Асинзронный клинет для поиска информации по API"""
        async with aiohttp.ClientSession() as session:
            async with session.get(**kwargs) as response:
                result = await response.json()
                return response.status, result

    async def _get_random_films(self) -> tuple[FilmModel, dict]:
        """Поиск случайного фильма."""

        search_film_params = {
            "page[size]": 1,
            "page[number]": random.randint(1, 100),
            "sort": "-imdb_rating",
        }

        endpoint = urljoin(settings.base_url+'search', f"?{urlencode(search_film_params)}")

        response_status, films = await self._get_data_from_http(url=endpoint)
        if response_status == status.HTTP_200_OK:
            logger.info('выбрали случайный фильм')
        else:
            logger.warning(f'ошибка запроса на url {endpoint}, статус {response_status}')

        uuid = films[0]['id']
        endpoint = urljoin(settings.base_url, f"{uuid}")
        full_film_data = await self._find_full_film_information(url=endpoint)
        logger.info('достали полную информацию по фильму')
        search_film_params['film_data'] = full_film_data.dict()

        return full_film_data, search_film_params

    # async def _get_films_by_genre(self, request: Request, genre: list) -> dict:
    #    """Поиск фильма по одному из жанров"""
    #    id_genre_for_recommendation = random.randint(0, len(genre) - 1)
    #    random_film = random.randint(1, 3)
    #
    #    search_film_params = {
    #        "page[size]": 1,
    #        "page[number]": random_film,
    #        "sort": "-imdb_rating",
    #        "genre": genre[id_genre_for_recommendation]
    #    }
    #    print('aaaaa', search_film_params)
    #    film_id = ''
    #    search_url = f'{request.base_url}api/v1/films'
    #
    #    status, film = await self._get_data_from_http(url=search_url, params=search_film_params)
    #    film_id = film[0].get('id')
    #
    #    film_information_url = f'{request.base_url}api/v1/films/{film_id}'
    #    return await self._find_full_film_information(url=film_information_url)

    async def _find_full_film_information(self, url: str) -> dict:
        """Получение полноой информации о фильме"""
        response_status, full_film_information = await self._get_data_from_http(url=url)
        if response_status == status.HTTP_200_OK:
            logger.info('выбрали случайный фильм')
        else:
            logger.warning(f'ошибка запроса на url {url}, статус {response_status}')

        film_model = FilmModel(**full_film_information)
        return film_model

    async def _recommendation_film(self, state: dict) -> tuple[str, dict]:
        """Поиск случайного фильма для рекомендации пользователю."""
        try:
            data_from_es, new_state = await self._get_random_films()
            logger.info('выбрали фильм')
            msg = data_from_es.title

        except Exception as e:
            logger.warning(e)
            msg = text_commands.film.error_response
        return msg, new_state

    # async def _context_answer_to_questions(self,
    #                                       state: dict, command: MarusyaRequestModel,
    #                                       request: Request,
    #                                       session_id: str) -> str:
    #    """Ответы пользователю в случае если он заходет узнать
    #    доп. информацию по рекомендованном фильме"""


#
#    phrase: str = text_commands.error
#
#    # Реакция на просьбу получить информацию о жанре в текущем фильме
#    if self._check_command(command, text_commands.context_film_to_genre.trigger_phrase):
#        phrase = ', '.join(state.get('genre'))
#
#    # Реакция на просьбу получить информацию об описании фильма
#    if self._check_command(command, text_commands.context_film_to_decription.trigger_phrase):
#        phrase = state.get('description', text_commands.context_film_to_decription.error_response)
#
#    # Реакция на просьбу получить информацию об актерах в фильме
#    if self._check_command(command, text_commands.context_film_to_actors.trigger_phrase):
#        if state.get('actors'):
#            phrase = ', '.join([c.get('name') for c in state.get('actors')])
#        else:
#            phrase = text_commands.context_film_to_actors.error_response
#
#    # Реакция на просьбу получить рекомендацию по фильму в таком же женре
#    if self._check_command(command, text_commands.context_genre.trigger_phrase):
#        if state.get('genre'):
#            try:
#                data_from_es = await self._get_films_by_genre(request=request,
#                                                              genre=state.get('genre'))
#                phrase = data_from_es.get('title')
#                await redis.redis.setex(session_id, settings.cache_expires, str(data_from_es))
#            except Exception:
#                phrase = text_commands.context_genre.error_response
#    return phrase


@lru_cache()
def get_alice_service() -> AliceService:
    return AliceService()
