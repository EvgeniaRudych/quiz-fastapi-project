import databases
import redis
from fastapi import FastAPI
import uvicorn

from config import system_config
from routers.todo import router
from databases import Database
from starlette.routing import Mount

app = FastAPI()
app.include_router(router)

db = databases.Database(system_config.db_url)
r = redis.Redis(host=system_config.redis_host, port=system_config.redis_port)




def inject_db(app: FastAPI, db: Database):
    app.state.database = db
    app.state.redis = r
    for route in app.router.routes:
        if isinstance(route, Mount):
            route.app.state.database = db
            route.app.state.redis = r


@app.on_event("startup")
async def startup():
    await db.connect()
    inject_db(app, db)


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
