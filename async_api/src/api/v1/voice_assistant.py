from random import randint
from fastapi import APIRouter, Depends
from services.film import film_list, get_film_description

from .deserializers.alice_deserializer import AliceRequest
from .serializers.alice_serializers import AliceResponse, AliceResponseModel
from .dependencies import (HELLO_TEXT,
                           EXIT_TEXT,
                           DANGEROUS_TEXT,
                           PARTING_TEXT,
                           OUT_OF_CONTEXT_TEXT,
                           MISUNDERSTAND_TEXT)


router = APIRouter()


@router.post("/voice", response_model = AliceResponseModel)
async def create_item(request: dict):
    alice_request = AliceRequest(**request)
    response = AliceResponse(alice_request.dict())

    if alice_request.session.new:
        response.set_text(HELLO_TEXT)
        response.set_buttons(EXIT_TEXT)
        return response.dumps()

    elif alice_request.request.markup.dangerous_context:
        response.set_text(DANGEROUS_TEXT)
        response.set_buttons(EXIT_TEXT)
        return response.dumps()

    elif 'exit' in  alice_request.request.nlu.intents:
        response.set_text(PARTING_TEXT)
        response.end()
        return response.dumps()

    elif 'get_film' in  alice_request.request.nlu.intents:
        page_number = randint(1, 999)
        films, film_id = await film_list(page_size=1,page_number=page_number)
        response.set_text(films)
        response.set_state(state_dict={'get_film': {'page_size':1,
                                                    'page_number': page_number,
                                                    'film_id': film_id}})
        response.set_buttons(EXIT_TEXT)
        return response.dumps()

    elif 'next' in alice_request.request.nlu.intents:
        get_film_state = alice_request.state['session'].get('get_film')
        if get_film_state:
            get_film_state['page_number'] += 1
            films = await film_list(get_film_state.get('page_size'), get_film_state.get('page_number'))
            response.set_text(films)
            response.set_state(alice_request.state['session'])
            response.set_buttons(EXIT_TEXT)
            return response.dumps()

        response.set_text(OUT_OF_CONTEXT_TEXT)
        return response.dumps()

    elif 'about_film' in alice_request.request.nlu.intents:
        description = await get_film_description(intents = alice_request.request.nlu.intents['about_film'])
        response.set_text(description)
        response.set_buttons(EXIT_TEXT)
        return response.dumps()

    elif 'about_film_context' in alice_request.request.nlu.intents:
        get_film_state = alice_request.state['session'].get('get_film')
        description = await get_film_description(state=get_film_state)
        response.set_text(description)
        response.set_buttons(EXIT_TEXT)
        return response.dumps()

    else:
        response.set_text(MISUNDERSTAND_TEXT)
        response.set_buttons(EXIT_TEXT)
        return response.dumps()


