from backend.app.seed import seed_clubs
from backend.app.seed.seed_drills import seed_drills

from pathlib import Path
from alembic.config import Config


BASE_DIR = Path(__file__).resolve().parents[2]  # стига до root
alembic_cfg = Config(str(BASE_DIR / "alembic.ini"))
