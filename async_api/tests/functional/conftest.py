import asyncio

import aiohttp
import aioredis
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch

from .settings import base_settings, film_settings, genre_settings, person_settings


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def es_client():
    async with AsyncElasticsearch(hosts=base_settings.es_host) as client:
        yield client
        # удаляем индексы после тестов
        await client.options(ignore_status=[400, 404]).indices.delete(
            index=(
                film_settings.es_index,
                person_settings.es_index,
                genre_settings.es_index,
            ),
            ignore_unavailable=True,
        )


@pytest_asyncio.fixture
async def redis_client():
    async with aioredis.from_url(f"redis://{base_settings.redis_host}:{base_settings.redis_port}") as client:
        async for key in client.scan_iter(match="*"):
            await client.delete(key)

        yield client


@pytest_asyncio.fixture(scope="session")
async def http_session():
    async with aiohttp.ClientSession() as session:
        yield session
