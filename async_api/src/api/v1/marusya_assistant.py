import random
import aiohttp

from core.config import settings
from core.voice_command.comand import text_commands
from fastapi import APIRouter, Depends, Request



from models.voice_model.marusya.request import MarusyaRequestModel
from models.voice_model.marusya.response import MarusyaResponseModel
from services.voice_assistent.mausya import get_marusya_service, MarusayService

router = APIRouter()

@router.post("/marusy",response_model= MarusyaResponseModel)
async def get_data_assistant(requestMarusya: MarusyaRequestModel,
                             request: Request,
                             marusya_service: MarusayService = Depends(get_marusya_service)):

    result = await marusya_service.get_data_assistant(requestMarusya=requestMarusya, request=request)
    return result
