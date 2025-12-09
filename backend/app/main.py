from fastapi import FastAPI

from .init_db import init_db
from .routers import auth

app = FastAPI(title="Volley Platform API")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


app.include_router(auth.router, prefix="/api")


@app.get("/")
def read_root():
    return {"status": "ok"}
