import uvicorn
from fastapi import FastAPI

app = FastAPI()

from routes.todo import router

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
