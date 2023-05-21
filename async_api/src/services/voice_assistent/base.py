
from abc import ABC, abstractmethod
from fastapi import Request

from pydantic import BaseModel


class Assistant(ABC):

    # Точка входя для общения с ассистентом
    @abstractmethod
    def get_data_assistant(self, requestAssistant: BaseModel, request: Request):
        ...
    # Метод валидации команд от ассистента
    @abstractmethod
    def _check_command(text_request: str, command: tuple):
        ...
    # Метод получения случайного фильма. 
    # В методе реализуется генерация случайного фильма
    @abstractmethod
    async def _get_random_films(self, request: Request) -> dict:
        ...
    # Метод поулчения фильма по жанру
    @abstractmethod
    async def _get_films_by_genre(self, request: Request, genre: list) -> dict:
        ...
    # Метод поулчения полной информации по фильму для реализации конекста и 
    # сообщения доп информации по запросу от ассистента
    @abstractmethod
    async def _find_full_film_information(self, url: str) -> dict:
        ...
    # Метод рекомендации фильма
    @abstractmethod
    async def _recommendation_film(self, session_id: str, request: Request) -> str:
        ...
    # Метод реакции на команды для уточнения информации 
    # по рекомендованному фильму. 
    @abstractmethod
    async def _context_answer_to_questions(self, state: dict,
                                           command: BaseModel, 
                                           request: Request,
                                           session_id: str) -> str:
        ...
    