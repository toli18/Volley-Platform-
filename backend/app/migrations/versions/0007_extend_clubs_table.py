from alembic import op
import sqlalchemy as sa

# === Alembic identifiers ===
revision = "0007_extend_clubs_table"
down_revision = "0006_add_country_to_clubs"
branch_labels = None
depends_on = None
# ===========================


def upgrade():
    op.add_column("clubs", sa.Column("address", sa.String(255)))
    op.add_column("clubs", sa.Column("contact_email", sa.String(255)))
    op.add_column("clubs", sa.Column("contact_phone", sa.String(255)))
    op.add_column("clubs", sa.Column("website_url", sa.String(255)))
    op.add_column("clubs", sa.Column("logo_url", sa.String(512)))


def downgrade():
    op.drop_column("clubs", "logo_url")
    op.drop_column("clubs", "website_url")
    op.drop_column("clubs", "contact_phone")
    op.drop_column("clubs", "contact_email")
    op.drop_column("clubs", "address")
