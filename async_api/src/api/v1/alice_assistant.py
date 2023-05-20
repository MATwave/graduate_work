from fastapi import APIRouter, Depends
from models.voice_model.alice.request import AliceRequestModel
from models.voice_model.alice.response import AliceResponseModel
from services.voice_assistent.alice import get_alice_service, AliceService

router = APIRouter()

@router.post("/voice",response_model= AliceResponseModel)
async def get_data_assistant(alice_request_model: AliceRequestModel,
                             alice_service: AliceService = Depends(get_alice_service)):

    result = await alice_service.get_data_assistant(alice_request_model)
    return result