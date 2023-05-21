from fastapi import APIRouter, Depends

from models.marusya.request import MarusyaRequestModel
from models.marusya.response import MarusyaResponseModel
from services.mausya import get_marusya_service, MarusayService
from fastapi_limiter.depends import RateLimiter

router = APIRouter()

@router.post("/marusya",response_model= MarusyaResponseModel, dependencies=[Depends(RateLimiter(times=15, seconds=10))])
async def get_data_assistant(requestMarusya: MarusyaRequestModel,
                             marusya_service: MarusayService = Depends(get_marusya_service)):

    result = await marusya_service.get_data_assistant(requestMarusya=requestMarusya)

    return result
