from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request
from databases import Database

app = FastAPI()


def get_database(request: Request) -> Database:
    return request.app.state.database
