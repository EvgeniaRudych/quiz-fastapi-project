import logging

from fastapi import APIRouter
from typing import Callable
from fastapi import FastAPI
from app.db.tasks import connect_to_db, close_db_connection
from pydantic import BaseSettings

router = APIRouter()


@router.get("/")
async def root():
    return {"status": "Working"}


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await connect_to_db(app)

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        await close_db_connection(app)

    return stop_app


class Config(BaseSettings):
    # The default URL expects the app to run using Docker and docker-compose.
    redis_url: str = 'redis://redis:6379'


log = logging.getLogger(__name__)
config = Config()
app = FastAPI(title='FastAPI Redis Tutorial')
redis = aioredis.from_url(config.redis_url, decode_responses=True)
