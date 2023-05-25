import logging
import random
from functools import lru_cache

import aiohttp
from src.core.config import settings
from src.core.voice_command.comand import text_commands
from src.models.marusya.request import MarusyaRequestModel
from src.models.marusya.response import MarusyaResponseModel, ResponseMarusya, Session
from src.services.base import Assistant

logger = logging.getLogger()


class MarusayService(Assistant):

    async def get_data_assistant(self, requestMarusya: MarusyaRequestModel) -> MarusyaResponseModel:
        """Основной метод для ызаимодействия с голосовым ассистенотм."""

        session_id = requestMarusya.session.session_id
        user_id = requestMarusya.session.user_id
        message_id = requestMarusya.session.message_id
        state: dict = self._get_current_state(requestMarusya=requestMarusya)
        resp = self._create_default_message(session_id=session_id, user_id=user_id, message_id=message_id, state=state)  # noqa: E501

        # Реакция на корректное завершение работы Маруси
        if self._check_command(requestMarusya.request.command, text_commands.end):
            resp.response.text, resp.response.end_session = self._create_bye_message()

        # Реакция на приветствие
        elif requestMarusya.session.new:
            resp.response.text = self._new_session_message()

        # Реакция на просьбу показать фильм
        elif self._check_command(requestMarusya.request.command, text_commands.film.trigger_phrase):
            resp.response.text, resp.session_state = await self._recommendation_film()

        # Ответ на вопросы по найденному фильму.
        elif state:
            resp.response.text, resp.session_state = await self._create_dialog(request=requestMarusya,
                                                                         session_id=session_id,
                                                                         state=state)
        return dict(resp)

    @staticmethod
    def _check_command(text_request: str, command: tuple) -> bool:
        """Метод для проверки запроса от ассистента со списом фразх на которы он должен реагировать."""
        for phrase in command:
            if phrase in text_request:
                return True
        return False


    async def _get_films(self) -> dict:
        """Поиск случайного фильма."""
        random_film = random.randint(1, 100)

        search_film_params = {
            "page[size]": 1,
            "page[number]": random_film,
            "sort": "-imdb_rating"
        }

        film_id = ''
        search_url = f'{settings.base_url}search'

        status_response, films = await self._get_data_from_http(url=search_url, params=search_film_params)
        logger.info(films)

        film_id = films[0].get('id')
        film_information_url = f'{settings.base_url}{film_id}'

        return await self._find_full_film_information(url=film_information_url)

    async def _get_films_by_genre(self, genre: list) -> dict:
        """Поиск фильма по одному из жанров"""
        id_genre_for_recommendation = random.randint(0, len(genre) - 1)
        random_film = random.randint(1, 3)

        search_film_params = {
            "page[size]": 1,
            "page[number]": random_film,
            "sort": "-imdb_rating",
            "genre": genre[id_genre_for_recommendation]
        }
        film_id = ''
        search_url = settings.base_url

        status_response, film = await self._get_data_from_http(url=search_url, params=search_film_params)
        logger.info(film)
        film_id = film[0].get('id')

        film_information_url = f'{settings.base_url}{film_id}'
        return await self._find_full_film_information(url=film_information_url)

    async def _find_full_film_information(self, url: str) -> dict:
        """Получение полноой информации о фильме"""
        status_response, full_film_information = await self._get_data_from_http(url=url)
        logger.info(full_film_information)
        return full_film_information

    async def _recommendation_film(self) -> str:
        """Поиск случайного фильма для рекомендации пользователю."""
        state = {}
        try:
            data_from_es = await self._get_films()
            state = data_from_es
            logger.info(data_from_es)
            msg = data_from_es.get('title')
        except Exception:
            msg = text_commands.film.error_response
        return msg, state

    async def _context_answer_to_questions(self,
                                           state: dict, command: MarusyaRequestModel,
                                           session_id: str) -> str:
        """Ответы пользователю в случае если он захочет узнать доп. информацию по рекомендованном фильме"""

        phrase: str = text_commands.error

        # Реакция на просьбу получить информацию о жанре в текущем фильме
        if self._check_command(command, text_commands.context_film_to_genre.trigger_phrase):
            phrase = ', '.join(state.get('genre'))

        # Реакция на просьбу получить информацию об описании фильма
        elif self._check_command(command, text_commands.context_film_to_decription.trigger_phrase):
            phrase = state.get('description', text_commands.context_film_to_decription.error_response)

        # Реакция на просьбу получить информацию об актерах в фильме
        elif self._check_command(command, text_commands.context_film_to_actors.trigger_phrase):
            if state.get('actors'):
                phrase = ', '.join([c.get('name') for c in state.get('actors')])
            else:
                phrase = text_commands.context_film_to_actors.error_response

        # Реакция на просьбу получить рекомендацию по фильму в таком же женре
        elif self._check_command(command, text_commands.context_genre.trigger_phrase):
            if state.get('genre'):
                try:
                    data_from_es = await self._get_films_by_genre(genre=state.get('genre'))
                    state = data_from_es
                    phrase = data_from_es.get('title')
                except Exception:
                    phrase = text_commands.context_genre.error_response
        return phrase, state

    def _create_default_message(self, session_id: str,
                                user_id: str,
                                message_id: str,
                                state: dict) -> MarusyaResponseModel:
        """Создаем объект по умолчанию, который будет возвращать Маруся,
        если не поймет команду"""
        return MarusyaResponseModel(response=ResponseMarusya(text=text_commands.error),
                                    session=Session(session_id=session_id,
                                                    user_id=user_id,
                                                    message_id=message_id),
                                    session_state=state
                )

    def _new_session_message(self) -> str:
        """Задаем преветственное сообщение"""
        return text_commands.welcome
    
    def _get_current_state(self, requestMarusya: MarusyaRequestModel) -> dict:
        """Получаем состояние диалога с Марусей"""
        state: dict = {}

        try:
            state = requestMarusya.state.session
            logger.info(f'Current state: {state}')
        except Exception as e:
            logger.exception(f'Exception get data from state as {e}')

        return state
    
    def _create_bye_message(self)->tuple:
        """Формируем сообщение завершения сессии и метку завершить сессию"""
        return text_commands.bye, True

    async def _create_dialog(self,
                             request: MarusyaRequestModel,
                             session_id: str,
                             state: dict)-> tuple:
       """Создаем диалог."""
       command: str = request.request.command
       phrase, state =  await self._context_answer_to_questions(command=command,
                                                                session_id=session_id,
                                                                state=state)
       return phrase, state

@lru_cache()
def get_marusya_service() -> MarusayService:
    return MarusayService()
