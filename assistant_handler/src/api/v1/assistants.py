from fastapi import APIRouter, Depends
from models.alice.request import AliceRequestModel
from models.alice.response import AliceResponseModel
from services.alice import get_alice_service, AliceService

from models.marusya.request import MarusyaRequestModel
from models.marusya.response import MarusyaResponseModel
from services.mausya import get_marusya_service, MarusayService

from fastapi_limiter.depends import RateLimiter

router = APIRouter()

@router.post("/voice",response_model= AliceResponseModel, dependencies=[Depends(RateLimiter(times=15, seconds=10))])
async def get_data_assistant(alice_request_model: AliceRequestModel,
                             alice_service: AliceService = Depends(get_alice_service)):

    result = await alice_service.get_data_assistant(alice_request_model)
    return result

@router.post("/marusya",response_model= MarusyaResponseModel, dependencies=[Depends(RateLimiter(times=15, seconds=10))])
async def get_data_assistant(requestMarusya: MarusyaRequestModel,
                             marusya_service: MarusayService = Depends(get_marusya_service)):

    result = await marusya_service.get_data_assistant(requestMarusya=requestMarusya)
    return result
