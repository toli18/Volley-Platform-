from fastapi import FastAPI
from backend.app.init_db import init_db, seed_platform_admin
from backend.app.seed.seed_clubs import seed_clubs
from backend.app.seed.seed_drills import seed_drills

app = FastAPI()

@app.on_event("startup")
def startup_event():
    print("🚀 Running migrations…")
    init_db()

    print("🌱 Seeding clubs…")
    try:
        seed_clubs()
    except Exception as e:
        print("❌ Clubs seeding failed:", e)

    print("🌱 Seeding drills…")
    try:
        seed_drills()
    except Exception as e:
        print("❌ Drills seeding failed:", e)

    print("👑 Creating admin…")
    try:
        seed_platform_admin()
    except Exception as e:
        print("❌ Admin seeding failed:", e)

    print("✅ Startup complete.")
