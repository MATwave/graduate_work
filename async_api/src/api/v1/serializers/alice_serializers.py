import json
from pydantic import BaseModel, Field

class AliceResponse(object):
    def __init__(self, alice_request):
        self._response_dict = {
            "version": alice_request.get('version'),
            "session": alice_request.get('session'),
            "response": {
                "end_session": False
            }
        }


    def dumps(self):
        return AliceResponseModel(** self._response_dict )

    def set_text(self, text):
        self._response_dict['response']['text'] = text[:1024]

    def set_buttons(self, buttons):
        self._response_dict['response']['buttons'] = buttons

    def end(self):
        self._response_dict["response"]["end_session"] = True



class AliceResponseModel(BaseModel):
    version: str = Field(..., example="1.0")
    session: dict
    response: dict