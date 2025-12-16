"""Change drills long text fields to TEXT

Revision ID: 0008_change_drills_columns_to_text
Revises: 0005_create_drills_table
Create Date: 2024-12-15
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0008_change_drills_columns_to_text"
down_revision = "0005_create_drills_table"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("drills", "skill_focus", type_=sa.Text())
    op.alter_column("drills", "goal", type_=sa.Text())
    op.alter_column("drills", "description", type_=sa.Text())
    op.alter_column("drills", "variations", type_=sa.Text())
    op.alter_column("drills", "players", type_=sa.Text())
    op.alter_column("drills", "equipment", type_=sa.Text())
    op.alter_column("drills", "image_urls", type_=sa.Text())
    op.alter_column("drills", "video_urls", type_=sa.Text())
    op.alter_column("drills", "skill_domains", type_=sa.Text())
    op.alter_column("drills", "game_phases", type_=sa.Text())
    op.alter_column("drills", "tactical_focus", type_=sa.Text())
    op.alter_column("drills", "technical_focus", type_=sa.Text())
    op.alter_column("drills", "position_focus", type_=sa.Text())
    op.alter_column("drills", "zone_focus", type_=sa.Text())
    op.alter_column("drills", "training_goal", type_=sa.Text())


def downgrade():
    op.alter_column("drills", "skill_focus", type_=sa.String(255))
    op.alter_column("drills", "goal", type_=sa.String(255))
    op.alter_column("drills", "description", type_=sa.String(255))
    op.alter_column("drills", "variations", type_=sa.String(255))
    op.alter_column("drills", "players", type_=sa.String(255))
    op.alter_column("drills", "equipment", type_=sa.String(255))
    op.alter_column("drills", "image_urls", type_=sa.String(255))
    op.alter_column("drills", "video_urls", type_=sa.String(255))
    op.alter_column("drills", "skill_domains", type_=sa.String(255))
    op.alter_column("drills", "game_phases", type_=sa.String(255))
    op.alter_column("drills", "tactical_focus", type_=sa.String(255))
    op.alter_column("drills", "technical_focus", type_=sa.String(255))
    op.alter_column("drills", "position_focus", type_=sa.String(255))
    op.alter_column("drills", "zone_focus", type_=sa.String(255))
    op.alter_column("drills", "training_goal", type_=sa.String(255))
