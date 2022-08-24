import logging

from fastapi import APIRouter
from typing import Callable
from fastapi import FastAPI
from pydantic import BaseSettings

router = APIRouter()


@router.get("/")
async def root():
    return {"status": "Working"}


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

