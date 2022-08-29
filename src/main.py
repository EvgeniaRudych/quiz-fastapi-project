import databases
from fastapi import FastAPI
import uvicorn
from config import system_config
from routers.todo import router
from databases import Database
from starlette.routing import Mount

app = FastAPI()
app.include_router(router)

db = databases.Database(system_config.db_url)


def inject_db(app: FastAPI, db: Database):
    app.state.database = db
    for route in app.router.routes:
        if isinstance(route, Mount):
            route.app.state.database = db


@app.on_event("startup")
async def startup():
    await db.connect()
    inject_db(app, db)


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
