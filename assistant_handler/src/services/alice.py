import random
from functools import lru_cache
from urllib.parse import urljoin, urlencode

import aiohttp
from fastapi import status, HTTPException
from loguru import logger
from src.core.config import settings
from src.core.voice_command.comand import text_commands
from src.models.alice.request import AliceRequestModel
from src.models.alice.response import AliceResponse, AliceResponseModel
from src.models.film import FilmModel
from src.services.base import Assistant


class AliceService(Assistant):

    @staticmethod
    def _check_command(text_request: str, command: dict) -> bool:
        """Метод для проверки запроса от ассистента со списом фразх на которы он должен реагировать."""
        return any(intent.startswith(text_request) for intent in command)

    async def get_data_assistant(self, alice_request_model: AliceRequestModel) -> AliceResponseModel:
        """Основной метод для взаимодействия с голосовым ассистентом."""

        response = AliceResponse(alice_request_model.dict())

        # Реакция на приветствие
        if alice_request_model.session.new:
            return await self.handle_greeting(response)

        # Реакция на выход
        elif self._check_command('exit', alice_request_model.request.nlu.intents):
            return await self.handle_exit(response)

        # Реакция на просьбу показать фильм
        elif self._check_command('get_film', alice_request_model.request.nlu.intents):
            return await self.handle_get_film(response)

        # Реакция на просьбу найти фильм
        elif self._check_command('film_search', alice_request_model.request.nlu.intents):
            return await self.handle_film_search(response, alice_request_model.request.nlu.intents["film_search"].slots)

        # Реакция на просьбу с контекстом
        elif self._check_command('about_film_context', alice_request_model.request.nlu.intents):
            return await self.handle_about_film_context(response, alice_request_model)

        # реакция на неизвестную просьбу
        else:
            return await self.handle_unknown_command(response, alice_request_model.request.command)

    async def handle_greeting(self, response: AliceResponse):
        logger.info('определили новую сессию')
        response.set_text(text_commands.welcome)
        response.set_buttons(text_commands.end[0])
        return response.dumps()

    async def handle_exit(self, response: AliceResponse):
        logger.info('определили интент exit')
        response.set_text(text_commands.bye)
        response.end()
        return response.dumps()

    async def handle_get_film(self, response: AliceResponse):
        logger.info('определили интент get_film')
        text, state = await self._recommendation_film(state=dict())
        response.set_text(text)
        response.set_state(state_dict={'get_film': state})
        response.set_buttons(text_commands.end[0])
        return response.dumps()

    async def handle_film_search(self, response: AliceResponse, slots):
        logger.info('определили интент film_search')
        text, state = await self._find_film(request=slots)
        response.set_text(text)
        response.set_state(state_dict={'get_film': state})
        response.set_buttons(text_commands.end[0])
        return response.dumps()

    async def handle_about_film_context(self, response: AliceResponse, alice_request_model: AliceRequestModel):
        logger.info('определили интент about_film_context')
        text, new_state = await self._context_answer_to_questions(request=alice_request_model)
        response.set_text(text)
        response.set_state(state_dict={'get_film': new_state})
        response.set_buttons(text_commands.end[0])
        return response.dumps()

    async def handle_unknown_command(self, response: AliceResponse, command):
        logger.warning(f'не поняли команды {command}')
        response.set_text(text_commands.error)
        response.set_buttons(text_commands.end[0])
        return response.dumps()

    async def _get_films(self, genre: list = None, title: str = None) -> tuple[FilmModel, dict]:
        """Поиск случайного фильма."""

        search_film_params = {
            "page[size]": 1,
            "page[number]": random.randint(1, 100) if title is None else 1,
            "sort": "-imdb_rating",
        }
        if genre:
            search_film_params["page[number]"] = random.randint(1, 3)
        elif title:
            search_film_params["query"] = title

        endpoint = urljoin(settings.base_url + 'search', f"?{urlencode(search_film_params)}")

        response_status, films = await self._get_data_from_http(url=endpoint)
        if response_status == status.HTTP_200_OK:
            logger.info('выбрали случайный фильм')
        else:
            logger.warning(f'ошибка запроса на url {endpoint}, статус {response_status}')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

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
            data_from_es, new_state = await self._get_films()
            logger.info('выбрали фильм')
            msg = data_from_es.title

        except Exception as e:
            logger.warning(e)
            msg = text_commands.film.error_response
            new_state = state

        return msg, new_state

    async def _find_film(self, request: AliceRequestModel) -> tuple[str, dict]:
        title = request['Film'].value
        try:
            data_from_es, new_state = await self._get_films(title=title)
            logger.info('нашли фильм')
            msg = data_from_es.title

        except Exception as e:
            logger.warning(e)
            msg = text_commands.film.error_response
            new_state = dict()

        return msg, new_state

    async def _context_answer_to_questions(self, request: AliceRequestModel) -> tuple[str, dict]:
        phrase: str = text_commands.error
        try:
            new_state = request.state['session']['get_film']
            film_data = request.state['session']['get_film']['film_data']
        except KeyError:
            new_state = request.state['session']
            phrase = text_commands.context_error
            return phrase, new_state

        # Реакция на просьбу получить информацию о жанре в текущем фильме
        if self._check_command('about_film_context_genre', request.request.nlu.intents):
            logger.info('определили интент about_genre')
            phrase = self._get_genre_response(film_data)

        # Реакция на просьбу получить информацию об описании фильма
        if self._check_command('about_film_context_description', request.request.nlu.intents):
            logger.info('определили интент about_description')
            phrase = self._get_description_response(film_data)

        # Реакция на просьбу получить информацию об актерах в фильме
        if self._check_command('about_film_context_actor', request.request.nlu.intents):
            logger.info('определили интент about_actors')
            phrase = self._get_actors_response(film_data)

        # Реакция на просьбу получить рекомендацию по фильму в таком же жанре
        if self._check_command('about_film_context_same_genre_film', request.request.nlu.intents):
            logger.info('определили интент about_same_genre_film')
            phrase, new_state = await self._get_same_genre_film_response(film_data)

        return phrase, new_state

    def _get_genre_response(self, film_data) -> str:
        phrase = ', '.join(film_data.get('genre', text_commands.context_film_to_genre.error_response))
        return phrase

    def _get_description_response(self, film_data) -> str:
        phrase = film_data.get('description', text_commands.context_film_to_decription.error_response)
        return phrase

    def _get_actors_response(self, film_data) -> str:
        actors = film_data.get('actors')
        if actors:
            return ', '.join(actor.get('name') for actor in actors)
        return text_commands.context_film_to_actors.error_response

    async def _get_same_genre_film_response(self, film_data) -> str:
        genre = film_data.get('genre')
        if genre:
            try:
                data_from_es, new_state = await self._get_films(genre=genre)
                return data_from_es.title, new_state
            except Exception as e:
                logger.warning(e)
                return text_commands.context_genre.error_response
        return text_commands.context_film_to_genre.error_response


@lru_cache()
def get_alice_service() -> AliceService:
    return AliceService()
