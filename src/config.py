import os
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()


class SystemConfig:
    app = FastAPI()
    db_key = os.getenv("SECRET_KEY")
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("POSTGRES_HOST")
    db_port = os.getenv("POSTGRES_PORT")
    db_name = os.getenv("POSTGRES_DB")
    redis_host = os.getenv("REDIS_HOST")
    redis_port = os.getenv("REDIS_PORT")
    db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


system_config = SystemConfig()
