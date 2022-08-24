import logging

from fastapi import APIRouter, Depends
from typing import Callable
from fastapi import FastAPI
from fastapi_framework import Redis, redis_dependency
from pydantic import BaseSettings

router = APIRouter()


@router.get("/")
async def root():
    return {"status": "Working"}


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@router.get("/set/{key}/{value}")
async def test(key: str, value: str, redis: Redis = Depends(redis_dependency)):
    await redis.set(key, value)
    return "Done"

