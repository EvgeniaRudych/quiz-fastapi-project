import redis
from starlette.requests import Request
from databases import Database


def get_database(request: Request) -> Database:
    return request.app.state.database


def get_redis(request: Request) -> redis.Redis:
    return request.app.state.redis
