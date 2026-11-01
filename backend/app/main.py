import redis
from fastapi import FastAPI
from redis.exceptions import RedisError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.config import settings
from app.db import engine

app = FastAPI(title="NetOps Portal API")


@app.get("/health")
def health():
    status = {"api": "ok", "mock_mode": settings.mock_mode}

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        status["database"] = "ok"
    except SQLAlchemyError as e:
        status["database"] = f"error: {e}"

    try:
        redis.from_url(settings.redis_url).ping()
        status["redis"] = "ok"
    except RedisError as e:
        status["redis"] = f"error: {e}"

    return status