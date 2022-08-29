from fastapi import APIRouter, Depends
from fastapi import Response
from fastapi.security import HTTPBearer
from starlette import status

from connections import get_redis
from utils import VerifyToken, get_user_info

router = APIRouter()


@router.get("/")
async def root():
    return {"status": "Working"}


@router.get("/set/{key}/{value}")
async def test(key: str, value: str, redis=Depends(get_redis)):
    redis.set(key, value)
    return redis.get(key)


@router.get("/api/v1/private")
async def private(token: str = Depends(get_user_info)):
    return token
