from alembic import op
import sqlalchemy as sa

# === Alembic identifiers ===
revision = "0006_add_country_to_clubs"
down_revision = "0005_create_drills_table"
branch_labels = None
depends_on = None
# ===========================


def upgrade():
    pass



def downgrade():
    op.drop_column("clubs", "country")
