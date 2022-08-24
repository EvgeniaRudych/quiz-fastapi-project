import sysconfig

import databases
import uvicorn
from fastapi import FastAPI, Depends
from routers.todo import router
from databases import Database
from starlette.requests import Request
from starlette.routing import Mount
from aioredis import Redis
from fastapi_framework import redis_dependency, database

app = FastAPI()
db = databases.Database(sysconfig.db_async_url)


def inject_db(app: FastApi, db: Database):
    app.state.database = db
    for route in app.router.routes:
        if isinstance(route, Mount):
            route.app.state.database = db


@app.on_event("startup")
async def startup():
    await database.connect(app, db)
    inject_db()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.on_event("startup")
async def on_startup():
    await redis_dependency.init()


@app.get("/set/{key}/{value}")
async def test(key: str, value: str, redis: Redis = Depends(redis_dependency)):
    await redis.set(key, value)
    return "Done"


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
