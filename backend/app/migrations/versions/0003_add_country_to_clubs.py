"""Add country column to clubs table"""

from alembic import op
import sqlalchemy as sa

revision = "0003_add_country_to_clubs"
down_revision = "0002_add_users_table"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    # If table doesn't exist yet → skip
    if "clubs" not in inspector.get_table_names():
        return

    columns = {col["name"] for col in inspector.get_columns("clubs")}

    # Add only if column does not exist
    if "country" not in columns:
        op.add_column("clubs", sa.Column("country", sa.String(255)))


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    # If table missing → skip
    if "clubs" not in inspector.get_table_names():
        return

    columns = {col["name"] for col in inspector.get_columns("clubs")}

    if "country" in columns:
        op.drop_column("clubs", "country")
