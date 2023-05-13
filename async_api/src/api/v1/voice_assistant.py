from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/voice")
async def create_item(item: dict):
    encoded_item = jsonable_encoder(item)
    return JSONResponse(content=encoded_item)