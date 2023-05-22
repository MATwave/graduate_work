import os

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()


class Settings(BaseSettings):
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_name: str = Field(..., env="FAST_API_PROJECT_NAME")
    base_url: str = Field(..., env="FAST_API_BASE_URL")
    redis_host: str = Field(..., env="REDIS_HOST")
    redis_port: int = Field(..., env="REDIS_PORT")

    class Config:
        env_file = ".env"


settings = Settings()
