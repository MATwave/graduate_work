from enum import Enum
import random
from functools import lru_cache
import uuid
from core.config import settings
from db import redis
from fastapi import APIRouter, Depends, Request
from urllib.parse import urljoin, urlencode
from core.voice_command.comand import text_commands
import aiohttp
import json
import logging


from models.marusya.request import MarusyaRequestModel
from models.marusya.response import MarusyaResponseModel, ResponseMarusya, Session
from services.base import Assistant

logger = logging.getLogger()


class MarusayService(Assistant):

    async def get_data_assistant(self, requestMarusya: MarusyaRequestModel) -> MarusyaResponseModel:
        """Основной метод для ызаимодействия с голосовым ассистенотм."""

        session_id = requestMarusya.session.session_id
        user_id = requestMarusya.session.user_id
        message_id = requestMarusya.session.message_id
        state: dict = {}
        last_state = await redis.redis.get(session_id)
        # Получаем последние данные которые запрашивали.
        # Тк данные хранятся на русском делаем манипуляции для преобразования его в JSON 
        if last_state:
            try:
                state = json.loads(last_state.replace("\'", "\""))
            except Exception as e:
                logger.exception(f'Exception decode data from redis as {e}')
                state = {}

        resp = MarusyaResponseModel(
                    response=ResponseMarusya(
                        text=text_commands.error),
                    session=Session(
                        session_id=session_id,
                        user_id=user_id,
                        message_id=message_id
                        )
                    )
        
        # Реакция на корректное завершение работы Маруси
        if self._check_command(requestMarusya.request.command, text_commands.end):
            resp.response.text = text_commands.bye
            resp.response.end_session=True
            return dict(resp)

        # Реакция на приветствие
        if requestMarusya.session.new:
            resp.response.text = text_commands.welcome 

        # Реакция на просьбу показать фильм
        if self._check_command(requestMarusya.request.command, text_commands.film.trigger_phrase):
            resp.response.text = await self._recommendation_film(session_id=session_id)
            return dict(resp)

        # Ответ на вопросы по найденному фильму.
        if state:
            resp.response.text = await self._context_answer_to_questions(command=requestMarusya.request.command,
                                                                         session_id=session_id,
                                                                         state=state)
            return dict(resp)

        return dict(resp)

    @staticmethod
    def _check_command(text_request: str, command: tuple) -> bool:
        """Метод для проверки запроса от ассистента со списом фразх на которы он должен реагировать."""
        for phrase in command:
            if phrase in text_request:
                return True
        return False

    async def _get_data_from_http(self, **kwargs):
        """Асинзронный клинет для поиска информации по API"""
        async with aiohttp.ClientSession() as session:
            async with session.get(**kwargs) as response:
                result = await response.json()
                return result
        
    async def _get_random_films(self) -> dict:
        """Поиск случайного фильма."""
        random_film = random.randint(1, 100)
        
        search_film_params = {
                    "page[size]": 1,
                    "page[number]": random_film,
                    "sort": "-imdb_rating"
                }

        film_id = ''
        search_url = f'{settings.base_url}search'

        films = await self._get_data_from_http(url=search_url, params=search_film_params)
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

        film = await self._get_data_from_http(url=search_url, params=search_film_params)
        logger.info(film)
        film_id = film[0].get('id')

        film_information_url = f'{settings.base_url}{film_id}'
        return await self._find_full_film_information(url=film_information_url)

    async def _find_full_film_information(self, url: str) -> dict:
        """Получение полноой информации о фильме"""
        full_film_information = await self._get_data_from_http(url=url)
        logger.info(full_film_information)
        return full_film_information

    async def _recommendation_film(self, session_id: str) -> str:
        """Поиск случайного фильма для рекомендации пользователю."""
        try:
            data_from_es = await self._get_random_films()
            logger.info(data_from_es)
            msg = data_from_es.get('title')
            await redis.redis.set( session_id, str(data_from_es), settings.cache_expires)
        except Exception:   
            msg = text_commands.film.error_response
        return msg
    
    async def _context_answer_to_questions(self,
                                           state: dict, command: MarusyaRequestModel,
                                           session_id: str)->str:
        """Ответы пользователю в случае если он заходет узнать 
        доп. информацию по рекомендованном фильме"""

        phrase: str = text_commands.error

        # Реакция на просьбу получить информацию о жанре в текущем фильме
        if self._check_command(command, text_commands.context_film_to_genre.trigger_phrase):
            phrase = ', '.join(state.get('genre'))
        
        # Реакция на просьбу получить информацию об описании фильма
        if self._check_command(command, text_commands.context_film_to_decription.trigger_phrase):
            phrase = state.get('description', text_commands.context_film_to_decription.error_response)

        # Реакция на просьбу получить информацию об актерах в фильме
        if self._check_command(command, text_commands.context_film_to_actors.trigger_phrase):
            if state.get('actors'):
                phrase = ', '.join([c.get('name') for c in state.get('actors')])
            else:
                phrase = text_commands.context_film_to_actors.error_response

        # Реакция на просьбу получить рекомендацию по фильму в таком же женре
        if self._check_command(command, text_commands.context_genre.trigger_phrase):
            if state.get('genre'):
                try:
                    data_from_es = await self._get_films_by_genre(genre=state.get('genre'))
                    phrase = data_from_es.get('title')
                    await redis.redis.set(session_id, str(data_from_es), settings.cache_expires)
                except Exception:   
                    phrase = text_commands.context_genre.error_response
        return phrase

@lru_cache()
def get_marusya_service() -> MarusayService:
    return MarusayService()