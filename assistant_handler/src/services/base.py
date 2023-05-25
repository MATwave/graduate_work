from abc import ABC, abstractmethod

from pydantic import BaseModel
import aiohttp


class Assistant(ABC):

    @abstractmethod
    def get_data_assistant(self, requestAssistant: BaseModel):
        """Точка входя для общения с ассистентом"""
        ...

    @abstractmethod
    def _check_command(text_request: str, command: tuple | dict):
        """Метод валидации команд от ассистента"""
        ...

    @abstractmethod
    async def _get_films(self) -> dict:
        """Метод получения случайного фильма."""
        ...

    @abstractmethod
    async def _find_full_film_information(self, url: str) -> dict:
        """Метод получения фильма по жанру"""
        ...

    @abstractmethod
    async def _recommendation_film(self, session_id: str) -> str:
        """Метод рекомендации фильма"""
        ...

    @abstractmethod
    async def _context_answer_to_questions(self, state: dict,
                                           command: BaseModel,
                                           session_id: str) -> str:
        """Метод реакции на команды для уточнения 
        информации по рекомендованному фильму."""
        ...

    async def _get_data_from_http(self, **kwargs):
        """Асинхронный клинет для поиска информации по API"""
        async with aiohttp.ClientSession() as session:
            async with session.get(**kwargs) as response:
                result = await response.json()
                return response.status, result