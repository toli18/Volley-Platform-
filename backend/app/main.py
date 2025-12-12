from fastapi import FastAPI
from backend.app.routers import auth, users, clubs, drills
from backend.app.init_db import init_db

app = FastAPI(title="Volley Platform API")

@app.on_event("startup")
def startup_event():
    init_db()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(clubs.router, prefix="/clubs", tags=["Clubs"])
app.include_router(drills.router, prefix="/drills", tags=["Drills"])
