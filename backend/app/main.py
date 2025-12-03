from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routers import auth, clubs, exercises, trainings, articles, forum, health
from backend.app.init_db import init_db

app = FastAPI(title="Volley Platform API")

# ... CORS middleware и include_router-ите, както си ги имаш ...


@app.on_event("startup")
def on_startup() -> None:
    """
    Тази функция се изпълнява всеки път,
    когато Uvicorn стартира приложението.
    """
    init_db()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(clubs.router)
app.include_router(exercises.router)
app.include_router(trainings.router)
app.include_router(articles.router)
app.include_router(forum.router)


@app.get("/")
def root():
    return {"message": "Volley Platform API", "endpoints": ["/auth/login", "/auth/me", "/exercises", "/trainings", "/clubs", "/articles", "/forum/categories"]}
