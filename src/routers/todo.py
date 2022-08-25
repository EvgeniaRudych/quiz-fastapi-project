from fastapi import APIRouter, Depends

from connections import get_redis

router = APIRouter()


@router.get("/")
async def root():
    return {"status": "Working"}


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@router.get("/set/{key}/{value}")
async def test(key: str, value: str, redis=Depends(get_redis)):
    redis.set(key, value)
    return redis.get(key)
