from pydantic import BaseModel, Field
import sys
from loguru import logger

class AliceResponse(object):
    def __init__(self, alice_request):
        self._response_dict = {
            "version": alice_request.get('version'),
            "session": alice_request.get('session'),
            "response": {
                "end_session": False
            },
            "session_state":{

            }
        }


    def dumps(self):
        return AliceResponseModel(** self._response_dict )

    def set_text(self, text: str):
        self._response_dict['response']['text'] = text[:1024]

    def set_buttons(self, buttons: str):
        self._response_dict['response']['buttons'] = [{'title':buttons, 'hide': True}]

    def set_state(self, state_dict: dict):
        size_in_kb = sys.getsizeof(state_dict) / 1024
        if size_in_kb <=1:
            logger.info(f"Размер JSON-объекта: {size_in_kb} Кб")
        else:
            logger.warning(f'Максимальный размер JSON-объекта session_state > 1 КБ (ограничение яндекс.Алисы'
                           f'https://yandex.ru/dev/dialogs/alice/doc/session-persistence.html)')
            state_dict = {}
        self._response_dict['session_state'] = state_dict

    def end(self):
        self._response_dict["response"]["end_session"] = True



class AliceResponseModel(BaseModel):
    version: str = Field(..., example="1.0")
    session: dict
    response: dict
    session_state: dict