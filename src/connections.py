import redis
from fastapi import FastAPI
from starlette.requests import Request
from databases import Database

from config import system_config

app = FastAPI()


def get_database(request: Request) -> Database:
    return request.app.state.database


def get_redis():
    return redis.Redis(host=system_config.redis_host, port=system_config.redis_port)
