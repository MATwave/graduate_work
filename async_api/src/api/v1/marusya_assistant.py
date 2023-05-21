from enum import Enum
import requests
from core.config import settings
from db import redis
from fastapi import APIRouter, Depends, Request
from urllib.parse import urljoin, urlencode
from .voice_command.comand import text_commands
import aiohttp
import json


from .deserializers.marusya_deserializer import MarusyaRequestModel
from .serializers.marusya_serializer import MarusyaResponseModel, ResponseMarusya, Buttons, Session

router = APIRouter()



@router.post("/marusya",response_model= MarusyaResponseModel)
async def get_data_assistant(requestMarusya: MarusyaRequestModel,
                             request: Request):

    session_id = requestMarusya.session.session_id
    user_id = requestMarusya.session.user_id
    message_id = requestMarusya.session.message_id
    state: dict = {}
    last_state = await redis.redis.get(session_id)

    # Получаем последние данные которые запрашивали.
    # Тк данные хранятся на русском делаем манипуляции для преобразования его в JSON 
    if last_state:
        state = json.loads(last_state.decode('utf8').replace("\'", "\""))


    resp = MarusyaResponseModel(
                response=ResponseMarusya(
                    text=text_commands.error),
                session=Session(
                    session_id=session_id,
                    user_id=user_id,
                    message_id=message_id
                    )
                )
    
    # # Реакция на приветствие
    if requestMarusya.session.new:
        resp.response.text = text_commands.welcome 
    # Реакция на просьбу показать фильм
    if _check_command(requestMarusya.request.command, text_commands.film):
        msg = ''
        try:
            data_from_es = await _get_films(request=request,
                                            phrase=requestMarusya.request.command)
            msg = data_from_es.get('title')
            await redis.redis.setex(session_id, settings.cache_expires, str(data_from_es))
        except Exception as e:    
            msg = 'Я не смогла найти данный фильм'

        resp.response.text = msg
        
    # Реакция на просьбу получить информацию о жанре в текущем фильме
    if _check_command(requestMarusya.request.command, text_commands.context_film_to_genre):
        if state:
            resp.response.text = ', '.join(state.get('genre'))
         #TODO: тут как-то надо обработать о том что делать если мы не знаем какой фильм запрашивался ранее
    
    # Реакция на просьбу получить информацию об описании фильма
    if _check_command(requestMarusya.request.command, text_commands.context_film_to_decription):
        if state:
            resp.response.text = state.get('description', 'Я не смоглда найти информацию о чем фильм')

    # Реакция на просьбу получить информацию об актерах в фильме
    if _check_command(requestMarusya.request.command, text_commands.context_film_to_actors):
        if state and state.get('actors'):
            resp.response.text = ', '.join([c.get('name') for c in state.get('actors')])


    # Реакция на корректное завершение работы Маруси
    if _check_command(requestMarusya.request.command, text_commands.end):
        resp.response.text = 'Рада помочь!'
        resp.response.end_session=True

                
    return dict(resp)


# TODO:  Вспамогательные функции вынести в отдельный модуль.

def _check_command(text_request: str, command: tuple) -> bool:
    for phrase in command:
        if phrase in text_request:
            return True
        return False
    
async def _get_films(request: Request, phrase: str) -> dict:
    search_film_params = {
            "page[size]": 1,
            "page[number]": 1,
            "sort": "-imdb_rating",
            "query": phrase
        }

    film_id = ''
    search_url = f'{request.base_url}api/v1/films/search'

    # TODO: обработать ошибку если ничего не найдено
    async with aiohttp.ClientSession() as session:
        # Поиск фильма по ключевым словам
        async with session.get(search_url, params=search_film_params) as response:
            film = await response.json()
            film_id = film[0].get('id')

        # Поик полной информации по фильму
        film_information_url = f'{request.base_url}api/v1/films/{film_id}'
        async with session.get(film_information_url) as response:
            result = await response.json()
            return result

