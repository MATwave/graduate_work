from contextlib import asynccontextmanager

import aioredis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi_limiter import FastAPILimiter
from src.api.v1 import assistants
from src.core.config import settings
from src.db import redis

origins = ["*"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis.redis = await aioredis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}",
                                          decode_responses=True)
    await FastAPILimiter.init(redis.redis)

    try:
        yield
    finally:
        await redis.redis.close()


app = FastAPI(
    lifespan=lifespan,
    title=settings.project_name,
    description="Эндпоинты для обработки запросов от голосовых помощников",
    docs_url="/api/openapi",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    openapi_tags=[
        {
            "name": "assistants",
            "description": "Эндпоинты обработки запросов от голосовых помощников",
        },
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assistants.router, prefix="/api/v1/assistants", tags=["assistants"])
