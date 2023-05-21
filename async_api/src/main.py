import aioredis
from api.v1 import films, genres, persons, alice_assistant, marusya_assistant
from core.config import settings
from db import elastic, redis
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

tags_metadata = [
    {
        "name": "films",
        "description": "Поиск фильмов",
    },
    {
        "name": "persons",
        "description": "Поиск персон (актеров, киноделов, сценаристов) и фильмов, в которых персона работала",
    },
    {
        "name": "genres",
        "description": "Поиск жанров",
    },
]

origins = ["*"]



app = FastAPI(
    title=settings.project_name,
    description="API для кинотеатра 🎥"
    "При помощи этого API возможно найти данные о "
    "любом интересующем вас фильме, доступной на сайте кинотеатра",
    docs_url="/api/openapi",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    redis.redis = await aioredis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}")

    elastic.es = AsyncElasticsearch(
        hosts=[f"{settings.elastic_host}:{settings.elastic_port}"]
    )


@app.on_event("shutdown")
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()

app.include_router(marusya_assistant.router, prefix="/api/v1/assistants/mausya", tags=["mausya"])
app.include_router(alice_assistant.router, prefix="/api/v1/assistants", tags=["alice"])
app.include_router(films.router, prefix="/api/v1/films", tags=["films"])
app.include_router(persons.router, prefix="/api/v1/persons", tags=["persons"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])
