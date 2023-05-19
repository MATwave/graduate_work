from enum import Enum
import random
from functools import lru_cache
from core.config import settings
from db import redis
from fastapi import APIRouter, Depends, Request
from urllib.parse import urljoin, urlencode
from core.voice_command.comand import text_commands
import aiohttp
import json


from models.voice_model.marusya.request import MarusyaRequestModel
from models.voice_model.marusya.response import MarusyaResponseModel, ResponseMarusya, Session


#TODO: Сюда перенести логику из ручки

# async def get_data_assistant(requestMarusya: MarusyaRequestModel,
#                                 request: Request):

#     session_id = requestMarusya.session.session_id
#     user_id = requestMarusya.session.user_id
#     message_id = requestMarusya.session.message_id
#     state: dict = {}
#     last_state = await redis.redis.get(session_id)

#     # Получаем последние данные которые запрашивали.
#     # Тк данные хранятся на русском делаем манипуляции для преобразования его в JSON 
#     if last_state:
#         state = json.loads(last_state.decode('utf8').replace("\'", "\""))

#     resp = MarusyaResponseModel(
#                 response=ResponseMarusya(
#                     text=text_commands.error),
#                 session=Session(
#                     session_id=session_id,
#                     user_id=user_id,
#                     message_id=message_id
#                     )
#                 )

#     # # Реакция на приветствие
#     if requestMarusya.session.new:
#         resp.response.text = text_commands.welcome 

    
#     # Реакция на просьбу показать фильм
#     if _check_command(requestMarusya.request.command, text_commands.film.trigger_phrase):
#         try:
#             data_from_es = await _get_films(request=request)
#             msg = data_from_es.get('title')
#             await redis.redis.setex(session_id, settings.cache_expires, str(data_from_es))
#         except Exception:   
#             msg = text_commands.film.error_response
#         resp.response.text = msg


#     if state:
#         # Реакция на просьбу получить информацию о жанре в текущем фильме
#         if _check_command(requestMarusya.request.command, text_commands.context_film_to_genre.trigger_phrase):
#             resp.response.text = ', '.join(state.get('genre'))
        
#         # Реакция на просьбу получить информацию об описании фильма
#         if _check_command(requestMarusya.request.command, text_commands.context_film_to_decription.trigger_phrase):
#             resp.response.text = state.get('description',
#                                             text_commands.context_film_to_decription.error_response)

#         # Реакция на просьбу получить информацию об актерах в фильме
#         if _check_command(requestMarusya.request.command, text_commands.context_film_to_actors.trigger_phrase):
#             if state.get('actors'):
#                 resp.response.text = ', '.join([c.get('name') for c in state.get('actors')])
#             else:
#                 resp.response.text = text_commands.context_film_to_actors.error_response

#         # Реакция на просьбу получить рекомендацию по фильму в таком же женре
#         if _check_command(requestMarusya.request.command, text_commands.context_genre.trigger_phrase):
#             if state.get('genre'):
#                 try:
#                     data_from_es = await _get_films_by_genre(request=request,
#                                                             genre=state.get('genre'))
#                     msg = data_from_es.get('title')
#                     await redis.redis.setex(session_id, settings.cache_expires, str(data_from_es))
#                 except Exception:   
#                     msg = text_commands.context_genre.error_response

#             resp.response.text = msg


#     # Реакция на корректное завершение работы Маруси
#     if _check_command(requestMarusya.request.command, text_commands.end):
#         resp.response.text = text_commands.bye
#         resp.response.end_session=True
#     print(dict(resp))
#     return dict(resp)


# async def _get_films(request: Request) -> dict:

#     random_film = random.randint(1, 100)
#     search_film_params = {
#                 "page[size]": 1,
#                 "page[number]": random_film,
#                 "sort": "-imdb_rating"
#             }

#     film_id = ''
#     search_url = f'{request.base_url}api/v1/films/search'

#     film = await _http_client(url=search_url, params=search_film_params)
#     film_id = film[0].get('id')

#     film_information_url = f'{request.base_url}api/v1/films/{film_id}'

#     result = await _http_client(url=film_information_url)
#     return result



# async def _get_films_by_genre(request: Request, genre: list) -> dict:

#     id_genre_for_recommendation = random.randint(0, len(genre) - 1)

#     random_film = random.randint(1, 100)
#     search_film_params = {
#                 "page[size]": 1,
#                 "page[number]": random_film,
#                 "sort": "-imdb_rating",
#                 "genre": genre[id_genre_for_recommendation]
#             }

#     film_id = ''
#     search_url = f'{request.base_url}api/v1/films'

#     film = await _http_client(url=search_url, params=search_film_params)
#     film_id = film[0].get('id')

#     film_information_url = f'{request.base_url}api/v1/films/{film_id}'

#     result = await _http_client(url=film_information_url)
#     return result


