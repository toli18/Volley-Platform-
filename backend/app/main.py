from fastapi import FastAPI

from .init_db import init_db

app = FastAPI(title="Volley Platform API")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/")
def read_root():
    return {"status": "ok"}
