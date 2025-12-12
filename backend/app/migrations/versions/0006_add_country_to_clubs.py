from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column(
        "clubs",
        sa.Column("country", sa.String(), nullable=True)
    )

def downgrade():
    op.drop_column("clubs", "country")
