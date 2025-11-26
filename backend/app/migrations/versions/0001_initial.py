from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "clubs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False, unique=True),
        sa.Column("city", sa.String(length=255)),
        sa.Column("logo_url", sa.String(length=512)),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("NOW()")),
    )

    user_role = sa.Enum("platform_admin", "bfv_admin", "coach", name="userrole")
    user_role.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.Column("club_id", sa.Integer(), sa.ForeignKey("clubs.id")),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("NOW()")),
    )

    op.create_table(
        "exercises",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("main_category", sa.String(length=255), nullable=False),
        sa.Column("sub_category", sa.String(length=255)),
        sa.Column("level", sa.String(length=100)),
        sa.Column("goal", sa.Text()),
        sa.Column("description", sa.Text()),
        sa.Column("players_required", sa.Integer()),
        sa.Column("intensity", sa.String(length=100)),
        sa.Column("duration_min", sa.Integer()),
        sa.Column("duration_max", sa.Integer()),
        sa.Column("tags", pg.JSONB(), server_default=pg.text("'[]'::jsonb")),
        sa.Column("age_groups", pg.JSONB(), server_default=pg.text("'[]'::jsonb")),
        sa.Column("image_urls", pg.JSONB(), server_default=pg.text("'[]'::jsonb")),
        sa.Column("video_urls", pg.JSONB(), server_default=pg.text("'[]'::jsonb")),
        sa.Column("created_by", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column("approved_by_admin", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("NOW()")),
    )

    op.create_table(
        "trainings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("club_id", sa.Integer(), sa.ForeignKey("clubs.id"), nullable=False),
        sa.Column("created_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("age_group", sa.String(length=100)),
        sa.Column("total_duration_min", sa.Integer()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("NOW()")),
    )

    op.create_table(
        "training_exercises",
        sa.Column("training_id", sa.Integer(), sa.ForeignKey("trainings.id"), primary_key=True),
        sa.Column("exercise_id", sa.Integer(), sa.ForeignKey("exercises.id"), primary_key=True),
        sa.Column("order_index", sa.Integer(), primary_key=True),
        sa.Column("custom_duration_min", sa.Integer()),
        sa.Column("notes", sa.Text()),
    )

    op.create_table(
        "exercise_suggestions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("main_category", sa.String(length=255)),
        sa.Column("description", sa.Text()),
        sa.Column("submitted_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("status", sa.String(length=50), server_default="pending"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("NOW()")),
        sa.Column("reviewed_by", sa.Integer(), sa.ForeignKey("users.id")),
    )

    op.create_table(
        "articles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=50), server_default="published"),
        sa.Column("created_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("approved_by", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("NOW()")),
    )

    op.create_table(
        "article_suggestions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("submitted_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("status", sa.String(length=50), server_default="pending"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("NOW()")),
        sa.Column("reviewed_by", sa.Integer(), sa.ForeignKey("users.id")),
    )

    op.create_table(
        "forum_categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("NOW()")),
    )

    op.create_table(
        "forum_topics",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("category_id", sa.Integer(), sa.ForeignKey("forum_categories.id"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("created_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("NOW()")),
    )

    op.create_table(
        "forum_posts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("topic_id", sa.Integer(), sa.ForeignKey("forum_topics.id"), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("NOW()")),
    )


def downgrade():
    op.drop_table("forum_posts")
    op.drop_table("forum_topics")
    op.drop_table("forum_categories")
    op.drop_table("article_suggestions")
    op.drop_table("articles")
    op.drop_table("exercise_suggestions")
    op.drop_table("training_exercises")
    op.drop_table("trainings")
    op.drop_table("exercises")
    op.drop_table("users")
    op.drop_table("clubs")
