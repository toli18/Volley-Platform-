"""Update userrole enum values"""

from alembic import op

revision = "0004_update_userrole_enum"
down_revision = "0003_add_country_to_clubs"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'platform_admin'")
    op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'bfv_admin'")
    op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'coach'")


def downgrade():
    pass
