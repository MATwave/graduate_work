from enum import Enum
import requests
from core.config import settings
from db import redis
from fastapi import APIRouter, Depends
from urllib.parse import urljoin, urlencode
from .voice_command.comand import text_commands


from .deserializers.marusya_deserializer import MarusyaRequestModel
from .serializers.marusya_serializer import MarusyaResponseModel, ResponseMarusya, Buttons, Session

router = APIRouter()



@router.post("/marusya", response_model= MarusyaResponseModel)
async def get_data_assistant(request: MarusyaRequestModel):
    session_id = request.session.session_id
    user_id = request.session.user_id
    message_id = request.session.message_id


    resp = MarusyaResponseModel(
                response=ResponseMarusya(
                    text=text_commands.error),
                session=Session(
                    session_id=session_id,
                    user_id=user_id,
                    message_id=message_id
                    )
                )
    
    if request.session.new:
        resp.response.text = text_commands.welcome 
    
    if _check_command(request.request.command, text_commands.film):
        resp.response.text = 'что то про фильм'
                
    if _check_command(request.request.command, text_commands.author):
        resp.response.text = 'Автор Антонша'
        print(request)
                
    return dict(resp)



def _check_command(text_request: str, command: Enum) -> bool:
    for phrase in command:
        if phrase in text_request:
            return True
        return False