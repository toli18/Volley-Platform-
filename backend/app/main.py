from fastapi import FastAPI
from backend.app.routers import auth, users, clubs, drills
from backend.app.init_db import init_db

app = FastAPI(title="Volley Platform API")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(auth, prefix="/auth", tags=["Auth"])
app.include_router(users, prefix="/users", tags=["Users"])
app.include_router(clubs, prefix="/clubs", tags=["Clubs"])
app.include_router(drills, prefix="/drills", tags=["Drills"])
