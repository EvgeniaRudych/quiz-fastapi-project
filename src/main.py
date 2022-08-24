import uvicorn
from fastapi import FastAPI
from routers.todo import router
from databases import Database
from starlette.requests import Request
from starlette.routing import Mount

app = FastAPI()


def inject_db(app: FastApi, db: Database):
    app.state.database = db
    for route in app.router.routes:
        if isinstance(route, Mount):
            route.app.state.database = db


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
