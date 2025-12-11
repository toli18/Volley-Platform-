from fastapi import FastAPI
from backend.app.init_db import init_db

app = FastAPI()

@app.on_event("startup")
def startup_event():
    print("🚀 Running migrations…")
    init_db()
    print("✅ Startup complete.")
