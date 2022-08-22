from main import app
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    return {"status": "Working"}


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
