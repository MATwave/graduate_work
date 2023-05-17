from enum import Enum
import requests
from core.config import settings
from db import redis
from fastapi import APIRouter, Depends, Request
from urllib.parse import urljoin, urlencode
from .voice_command.comand import text_commands
import aiohttp


from .deserializers.marusya_deserializer import MarusyaRequestModel
from .serializers.marusya_serializer import MarusyaResponseModel, ResponseMarusya, Buttons, Session

router = APIRouter()



@router.post("/marusya",response_model= MarusyaResponseModel)

async def get_data_assistant(requestMarusya: MarusyaRequestModel,
                             request: Request):
    print(request.base_url)
    session_id = requestMarusya.session.session_id
    user_id = requestMarusya.session.user_id
    message_id = requestMarusya.session.message_id

    last_state = await redis.redis.get(session_id)

    await redis.redis.setex(session_id,
                            settings.cache_expires,
                            str({'aaa':1}))

    resp = MarusyaResponseModel(
                response=ResponseMarusya(
                    text=text_commands.error),
                session=Session(
                    session_id=session_id,
                    user_id=user_id,
                    message_id=message_id
                    )
                )
    

    if requestMarusya.session.new:
        resp.response.text = text_commands.welcome 
    
    if _check_command(requestMarusya.request.command, text_commands.film):
        url = f'{request.base_url}/api/v1/films/search'
        params = {
            "page[size]": 1,
            "page[number]": 1,
            "sort": "-imdb_rating"
        }
        data_from_es = await _get_films(url=url, params=params)[0]
        resp.response.text = 'что то про фильм'
                
    if _check_command(requestMarusya.request.command, text_commands.author):
        resp.response.text = 'Автор'

                
    return dict(resp)



def _check_command(text_request: str, command: tuple) -> bool:
    for phrase in command:
        if phrase in text_request:
            return True
        return False
    

async def _get_films(url: str, params: dict) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get('http://python.org', json=params) as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            result = await response.text()

