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
        response.set_text('Это навык Фильмо Вед - голосовой ассистент для кинотеатра! Вот что я умею:\n'
                          'Скажи "Посоветуй фильм", если захочешь другой - скажи "ещё". '
                          'Если захочешь узнать описание фильма - спроси "о чем <название фильма>"')
        response.set_buttons('Выйти из навыка')
        return response.dumps()

    elif alice_request.request.markup.dangerous_context:
        response.set_text('Опасные вещи говорите!')
        response.set_buttons('Выйти из навыка')
        return response.dumps()

    elif 'exit' in  alice_request.request.nlu.intents:
        response.set_text('Пока-пока. Приходи еще!')
        response.end()
        return response.dumps()

    elif 'get_film' in  alice_request.request.nlu.intents:
        films = await film_list(int(page_number) if page_number is not None else 1)
        await redis.redis.setex(session_id, settings.cache_expires, str(int(page_number) + 1) if page_number else "2")
        response.set_text(films)
        response.set_buttons('Выйти из навыка')
        return response.dumps()

    elif 'next' in alice_request.request.nlu.intents:
        if page_number:
            films = await film_list(int(page_number))
            await redis.redis.setex(session_id, settings.cache_expires, str(int(page_number) + 1))
            response.set_text(films)
            response.set_buttons('Выйти из навыка')
            return response.dumps()

        response.set_text('Нет доступных фильмов.')
        return response.dumps()

    elif 'about_film' in alice_request.request.nlu.intents:
        description = await get_film_description(alice_request.request.nlu.intents['about_film'])
        response.set_text(description)
        response.set_buttons('Выйти из навыка')
        return response.dumps()

    else:
        response.set_text('Не понимаю вашей команды!')
        response.set_buttons('Выйти из навыка')
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

            response_text = 'Советую фильм: '
            for film in film_list:
                response_text += f"{film['title']}, "
                response_text += f"Рейтинг IMDB: {film['imdb_rating']}, "
                response_text += f"Жанр: {', '.join(film['genre'])}, "

            if len(film_list) == 0:
                response_text = 'Фильмы в моем списке кончились.'

        return response_text

    except requests.exceptions.RequestException as e:
        return 'Ошибка при получении данных о фильмах.'

async def get_film_description(slots):
    film = slots.get('slots', {}).get('Film', {}).get('value')
    base_url = settings.base_url + 'search'
    params = {
        "page[size]": 1,
        "page[number]": 1,
        "query": film
    }
    query_string = urlencode(params)
    endpoint = urljoin(base_url, f"?{query_string}")
    try:
        with requests.get(endpoint) as response:
            response.raise_for_status()
            films = response.json()

            response_text = f'Подробнее о фильме "{film}": '
            if len(films) == 0:
                response_text = f'Не нашла у себя фильм "{film}".'

            elif len(films) == 1:
                uuid = films[0]['id']
                endpoint = urljoin(base_url, f"{uuid}")
                print(endpoint)
                with requests.get(endpoint) as response:
                    response.raise_for_status()
                    description = response.json()['description']
                    response_text += description

        return response_text

    except requests.exceptions.RequestException as e:
        return 'Ошибка при получении данных о фильмах.'