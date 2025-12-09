from backend.app.seed import seed_clubs

from pathlib import Path
from alembic.config import Config

BASE_DIR = Path(__file__).resolve().parents[2]  # стига до root
alembic_cfg = Config(str(BASE_DIR / "alembic.ini"))
