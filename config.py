import logging
import aioredis as aioredis
from databases import DatabaseURL
from fastapi import FastAPI
from pydantic import BaseSettings
from starlette.config import Config
from starlette.datastructures import Secret


class Config(BaseSettings):
    config = Config()
    redis_url: str = 'redis://redis:6379'
    log = logging.getLogger(__name__)
    app = FastAPI(title='FastAPI Redis Tutorial')
    redis = aioredis.from_url(config.redis_url, decode_responses=True)
    SECRET_KEY = config("SECRET_KEY", cast=Secret, default="CHANGEME")
    POSTGRES_USER = config("POSTGRES_USER", cast=str)
    POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
    POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str, default="db")
    POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
    POSTGRES_DB = config("POSTGRES_DB", cast=str)
    DATABASE_URL = config(
        "DATABASE_URL",
        cast=DatabaseURL,
        default=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
