"""Fix foreign key constraints with SET NULL on delete

Revision ID: 8f53ea94b63d
Revises: 6a1f35242e5b
Create Date: 2025-06-21 08:43:52.920766

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8f53ea94b63d"
down_revision: Union[str, None] = "6a1f35242e5b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("articles", sa.Column("last_modified_by_user_id", sa.Integer(), nullable=True))
    op.create_index(
        op.f("ix_articles_last_modified_by_user_id"),
        "articles",
        ["last_modified_by_user_id"],
        unique=False,
    )
    op.drop_constraint(op.f("articles_primary_character_id_fkey"), "articles", type_="foreignkey")
    op.drop_constraint(op.f("articles_primary_location_id_fkey"), "articles", type_="foreignkey")
    op.drop_constraint(op.f("articles_primary_faction_id_fkey"), "articles", type_="foreignkey")
    op.drop_constraint(op.f("articles_primary_race_id_fkey"), "articles", type_="foreignkey")
    op.create_foreign_key(
        None,
        "articles",
        "locations",
        ["primary_location_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        None,
        "articles",
        "characters",
        ["primary_character_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(None, "articles", "users", ["last_modified_by_user_id"], ["id"])
    op.create_foreign_key(
        None,
        "articles",
        "factions",
        ["primary_faction_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(None, "articles", "races", ["primary_race_id"], ["id"], ondelete="SET NULL")
    op.drop_constraint(op.f("characters_race_id_fkey"), "characters", type_="foreignkey")
    op.create_foreign_key(None, "characters", "races", ["race_id"], ["id"], ondelete="SET NULL")
    op.create_index(
        "idx_faction_structure",
        "faction_culture",
        ["internal_structure"],
        unique=False,
        postgresql_using="gin",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("idx_faction_structure", table_name="faction_culture", postgresql_using="gin")
    op.drop_constraint(None, "characters", type_="foreignkey")
    op.create_foreign_key(op.f("characters_race_id_fkey"), "characters", "races", ["race_id"], ["id"])
    op.drop_constraint(None, "articles", type_="foreignkey")
    op.drop_constraint(None, "articles", type_="foreignkey")
    op.drop_constraint(None, "articles", type_="foreignkey")
    op.drop_constraint(None, "articles", type_="foreignkey")
    op.drop_constraint(None, "articles", type_="foreignkey")
    op.create_foreign_key(
        op.f("articles_primary_race_id_fkey"),
        "articles",
        "races",
        ["primary_race_id"],
        ["id"],
    )
    op.create_foreign_key(
        op.f("articles_primary_faction_id_fkey"),
        "articles",
        "factions",
        ["primary_faction_id"],
        ["id"],
    )
    op.create_foreign_key(
        op.f("articles_primary_location_id_fkey"),
        "articles",
        "locations",
        ["primary_location_id"],
        ["id"],
    )
    op.create_foreign_key(
        op.f("articles_primary_character_id_fkey"),
        "articles",
        "characters",
        ["primary_character_id"],
        ["id"],
    )
    op.drop_index(op.f("ix_articles_last_modified_by_user_id"), table_name="articles")
    op.drop_column("articles", "last_modified_by_user_id")
    # ### end Alembic commands ###
