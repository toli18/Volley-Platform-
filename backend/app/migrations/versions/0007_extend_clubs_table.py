from alembic import op
import sqlalchemy as sa

# === Alembic identifiers ===
revision = "0007_extend_clubs_table"
down_revision = "0006_add_country_to_clubs"
branch_labels = None
depends_on = None
# ===========================


def upgrade():
    pass


def downgrade():
    op.drop_column("clubs", "website_url")
    op.drop_column("clubs", "contact_phone")
    op.drop_column("clubs", "contact_email")
    op.drop_column("clubs", "address")
