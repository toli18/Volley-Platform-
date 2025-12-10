"""Add country column to clubs table"""

from alembic import op
import sqlalchemy as sa

revision = "0003_add_country_to_clubs"
down_revision = "0002_add_users_table"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("clubs", sa.Column("country", sa.String(255)))


def downgrade():
    op.drop_column("clubs", "country")

