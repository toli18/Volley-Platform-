# Volley-Platform-

Volley Platform Единната система за тренировки, упражнения и методика по волейбол.

## Running locally

1. Install dependencies with Poetry (Python 3.11):

```bash
pip install "poetry>=1.8" && poetry install --no-root
```

2. Run database migrations and start the API:

```bash
poetry run alembic upgrade head && poetry run uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

The same command is used by Render during deployment.

## Database seeding

Seed data for clubs is stored in `backend/app/seed/clubs.csv`. The application loads missing rows during startup via `init_db()`.
