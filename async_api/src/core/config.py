import os
from logging import config as logging_config

from core.logger import LOGGING
from dotenv import load_dotenv
from pydantic import BaseSettings, Field

logging_config.dictConfig(LOGGING)
load_dotenv()


class Settings(BaseSettings):
    es_index: str | None = None
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_name: str = Field(..., env="FAST_API_PROJECT_NAME")
    base_url: str = Field(..., env="FAST_API_BASE_URL")
    redis_host: str = Field(..., env="REDIS_HOST")
    redis_port: int = Field(..., env="REDIS_PORT")
    elastic_host: str = Field(..., env="ELASTIC_HOST")
    elastic_port: int = Field(..., env="ELASTIC_PORT")

    cache_expires: int = 60 * 5

    class Config:
        env_file = ".env"


settings = Settings()
film_settings = Settings(
    es_index=os.getenv("ELASTIC_FILM_ES_INDEX"),
)
person_settings = Settings(
    es_index=os.getenv("ELASTIC_PERSON_ES_INDEX"),
)
genre_settings = Settings(
    es_index=os.getenv("ELASTIC_GENRE_ES_INDEX"),
)
