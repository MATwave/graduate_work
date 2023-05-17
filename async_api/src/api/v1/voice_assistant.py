import requests
from core.config import settings
from db import redis
from fastapi import APIRouter, Depends
from urllib.parse import urljoin, urlencode

from .deserializers.alice_deserializer import AliceRequest
from .serializers.alice_serializers import AliceResponse, AliceResponseModel

router = APIRouter()


@router.post("/voice", response_model = AliceResponseModel)
async def create_item(request: dict):
    alice_request = AliceRequest(**request)
    response = AliceResponse(alice_request.dict())
    session_id = alice_request.session.session_id
    page_number = await redis.redis.get(session_id)

    if alice_request.session.new:
        response.set_text('Это навык Фильмо Вед - голосовой ассистент для кинотеатра! Вот что я умею:'
                          'Скажи "Посоветуй фильм", если захочешь другой - скажи "ещё"')
        return response.dumps()

    elif alice_request.request.markup.dangerous_context:
        response.set_text('Опасные вещи говорите!')
        return response.dumps()

    elif alice_request.request.command == 'посоветуй фильм':
        films = await film_list(int(page_number) if page_number is not None else 1)
        await redis.redis.setex(session_id, settings.cache_expires, str(int(page_number) + 1) if page_number else "2")
        response.set_text(films)
        return response.dumps()

    elif alice_request.request.command == 'еще':
        if page_number:
            films = await film_list(int(page_number))
            await redis.redis.setex(session_id, settings.cache_expires, str(int(page_number) + 1))
            response.set_text(films)
            return response.dumps()

        response.set_text('Нет доступных фильмов.')
        return response.dumps()
    else:
        response.set_text('Не понимаю вашей команды!')
        return response.dumps()


async def film_list(page_number):
    base_url = settings.base_url
    params = {
        "page[size]": 1,
        "page[number]": page_number
    }
    query_string = urlencode(params)
    endpoint = urljoin(base_url, f"?{query_string}")
    try:
        with requests.get(endpoint) as response:
            response.raise_for_status()
            films = response.json()

            film_list = [
                {
                    'id': film['id'],
                    'title': film['title'],
                    'imdb_rating': film['imdb_rating'],
                    'genre': film['genre']
                }
                for film in films
            ]

            response_text = 'Список фильмов: '
            for film in film_list:
                response_text += f"Название: {film['title']}, "
                response_text += f"Рейтинг IMDB: {film['imdb_rating']}, "
                response_text += f"Жанры: {', '.join(film['genre'])}, "

            if len(film_list) == 0:
                response_text = 'Фильмы в моем списке кончились.'

        return response_text

    except requests.exceptions.RequestException as e:
        return 'Ошибка при получении данных о фильмах.'
