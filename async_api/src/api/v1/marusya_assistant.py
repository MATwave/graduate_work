from fastapi import APIRouter, Depends, Request

from models.voice_model.marusya.request import MarusyaRequestModel
from models.voice_model.marusya.response import MarusyaResponseModel
from services.voice_assistent.mausya import get_marusya_service, MarusayService
from fastapi_limiter.depends import RateLimiter

router = APIRouter()

@router.post("/marusya",response_model= MarusyaResponseModel, dependencies=[Depends(RateLimiter(times=1000, hours=1))])
async def get_data_assistant(requestMarusya: MarusyaRequestModel,
                             request: Request,
                             marusya_service: MarusayService = Depends(get_marusya_service)):

    result = await marusya_service.get_data_assistant(requestMarusya=requestMarusya, request=request)

    return result
