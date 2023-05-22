import aioredis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi_limiter import FastAPILimiter

from api.v1 import assistants
from core.config import settings
from db import redis

origins = ["*"]

app = FastAPI(
    title=settings.project_name,
    description="Эндпоинты для обработки запросов от голосовых помощников",
    docs_url="/api/openapi",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    openapi_tags=[
        {
            "name": "mausya",
            "description": "Эндпоинт обработки запросов от голосового помощника Маруси",
        },
        {
            "name": "alice",
            "description": "Эндпоинт обработки запросов от голосового помощника Алисы",
        },

    ],
)


@app.on_event("startup")
async def startup():
    redis.redis = await aioredis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}", decode_responses=True)
    await FastAPILimiter.init(redis.redis)


@app.on_event("shutdown")
async def shutdown():
    await redis.redis.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assistants.router, prefix="/api/v1/assistants", tags=["assistants"])
