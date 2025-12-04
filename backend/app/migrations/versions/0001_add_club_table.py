"""add club table"""

from alembic import op
import sqlalchemy as sa

revision = "0001_add_club_table"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "clubs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("city", sa.String(255)),
        sa.Column("address", sa.String(255)),
        sa.Column("contact_email", sa.String(255)),
        sa.Column("contact_phone", sa.String(255)),
        sa.Column("website_url", sa.String(255)),
        sa.Column("logo_url", sa.String(512)),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
    )


def downgrade():
    op.drop_table("clubs")
