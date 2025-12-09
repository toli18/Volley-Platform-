from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from pathlib import Path

# ✅ ЗАДЪЛЖИТЕЛНО ТОВА:
config = context.config

# ✅ ROOT пътя:
BASE_DIR = Path(__file__).resolve().parents[3]
alembic_ini_path = BASE_DIR / "alembic.ini"

# ✅ Подаваме правилния alembic.ini:
config.config_file_name = str(alembic_ini_path)

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)
