import os

import redis
from fastapi import FastAPI, HTTPException

app = FastAPI()
r = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379, decode_responses=True)


@app.get("/healthz")
def healthz():
    try:
        r.ping()
    except redis.RedisError:
        raise HTTPException(status_code=503, detail="Redis unavailable")
    return {"status": "ok", "redis": "up"}


@app.post("/hit/{key}")
def hit(key: str):
    try:
        count = r.incr(f"counter:{key}")
    except redis.RedisError:
        raise HTTPException(status_code=503, detail="Redis unavailable")
    return {"key": key, "count": count}


@app.get("/count/{key}")
def count(key: str):
    try:
        value = r.get(f"counter:{key}")
    except redis.RedisError:
        raise HTTPException(status_code=503, detail="Redis unavailable")
    return {"key": key, "count": int(value) if value is not None else 0}
