def run_alembic():
    alembic_cfg = Config(str(settings.alembic_ini_path))
    alembic_cfg.set_main_option("script_location", str(settings.migrations_path))
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url)

    command.upgrade(alembic_cfg, "head")
    print("✅ Alembic migrations applied.")


def init_db() -> None:
    """Initialize DB, run migrations, seed data."""
    try:
        # 🔥 ONLY Alembic controls schema
        run_alembic()

        # Seed data (idempotent)
        seed_platform_admin()
        seed_clubs()
        seed_drills()

        print("✅ Database initialization complete.")

    except Exception as exc:
        print("❌ DB initialization failed:", exc)
        raise
