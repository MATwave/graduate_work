import random
from functools import lru_cache
from urllib.parse import urljoin, urlencode

import aiohttp
from core.config import settings
from core.voice_command.comand import text_commands
from fastapi import status, HTTPException
from loguru import logger
from models.film import FilmModel
from models.voice_model.alice.request import AliceRequestModel
from models.voice_model.alice.response import AliceResponse, AliceResponseModel


class AliceService:

    async def get_data_assistant(self, alice_request_model: AliceRequestModel) -> AliceResponseModel:
        """Основной метод для взаимодействия с голосовым ассистентом."""

        response = AliceResponse(alice_request_model.dict())

        # Реакция на приветствие
        if alice_request_model.session.new:
            logger.info('определили новую сессию')
            response.set_text(text_commands.welcome)
            response.set_buttons(text_commands.end[0])
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
            response.set_buttons(text_commands.end[0])
            return response.dumps()

        elif any(intent.startswith("about_film_context") for intent in alice_request_model.request.nlu.intents):
            logger.info('определили интент about_film_context')
            get_film_state = alice_request_model.state['session']['get_film'].get('film_data')
            text = await self._context_answer_to_questions(state=get_film_state, request=alice_request_model)
            response.set_text(text)
            response.set_state(state_dict={'get_film': alice_request_model.state['session']})
            response.set_buttons(text_commands.end[0])
            return response.dumps()

        else:
            logger.info('не поняли команды')
            response.set_text(text_commands.error)
            response.set_buttons(text_commands.end[0])
            return response.dumps()

    async def _get_data_from_http(self, **kwargs):
        """Асинзронный клинет для поиска информации по API"""
        async with aiohttp.ClientSession() as session:
            async with session.get(**kwargs) as response:
                result = await response.json()
                return response.status, result

    async def _get_random_films(self, genre: list = None) -> tuple[FilmModel, dict]:
        """Поиск случайного фильма."""

        search_film_params = {
            "page[size]": 1,
            "page[number]": random.randint(1, 100),
            "sort": "-imdb_rating",
        }
        if genre:
            search_film_params["page[number]"] = random.randint(1, 3)

        endpoint = urljoin(settings.base_url+'search', f"?{urlencode(search_film_params)}")

        response_status, films = await self._get_data_from_http(url=endpoint)
        if response_status == status.HTTP_200_OK:
            logger.info('выбрали случайный фильм')
        else:
            logger.warning(f'ошибка запроса на url {endpoint}, статус {response_status}')
            raise HTTPException(status_code=404, detail="Not Found")

        film_uuid = films[0]['id']
        endpoint = urljoin(settings.base_url, f"{film_uuid}")
        full_film_data = await self._find_full_film_information(url=endpoint)
        logger.info('достали полную информацию по фильму')
        search_film_params['film_data'] = full_film_data.dict()

        return full_film_data, search_film_params

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
            new_state = state

        return msg, new_state

    async def _context_answer_to_questions(self, state: dict, request: AliceRequestModel) -> tuple[str, dict]:
        logger.info(state)

        phrase: str = text_commands.error
        new_state = state

        # Реакция на просьбу получить информацию о жанре в текущем фильме
        if 'about_film_context_genre' in request.request.nlu.intents:
            logger.info('определили интент about_genre')
            phrase = ', '.join(state.get('genre'), text_commands.context_film_to_genre.error_response)

        # Реакция на просьбу получить информацию об описании фильма
        if 'about_film_context_description' in request.request.nlu.intents:
            logger.info('определили интент about_description')
            phrase = state.get('description', text_commands.context_film_to_decription.error_response)

        # Реакция на просьбу получить информацию об актерах в фильме
        if 'about_film_context_actor' in request.request.nlu.intents:
            logger.info('определили интент about_actors')
            if state.get('actors'):
                phrase = ', '.join([c.get('name') for c in state.get('actors')])
            else:
                phrase = text_commands.context_film_to_actors.error_response

        # Реакция на просьбу получить рекомендацию по фильму в таком же жанре
        if 'about_film_context_same_genre_film' in request.request.nlu.intents:
            logger.info('определили интент about_same_genre_film')
            if state.get('genre'):
                try:
                    data_from_es, new_state = await self._get_random_films(genre=state.get('genre'))
                    phrase = data_from_es.title
                except Exception as e:
                    logger.warning(e)
                    phrase = text_commands.context_genre.error_response
            else:
                phrase = text_commands.context_film_to_genre.error_response

        return phrase, new_state


@lru_cache()
def get_alice_service() -> AliceService:
    return AliceService()
