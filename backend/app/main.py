from fastapi import FastAPI

from backend.app.routers import auth, users, clubs, drills

app = FastAPI(title="Volley Platform API")


@app.get("/")
def root():
    return {"status": "Volley Platform API is running"}


app.include_router(auth, prefix="/auth", tags=["Auth"])
app.include_router(users, prefix="/users", tags=["Users"])
app.include_router(clubs, prefix="/clubs", tags=["Clubs"])
app.include_router(drills, prefix="/drills", tags=["Drills"])
