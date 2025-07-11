"""add new models: ability and class

Revision ID: dba07ba91bdc
Revises: 15f5f15641e8
Create Date: 2025-07-04 09:19:12.785778

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "dba07ba91bdc"
down_revision: Union[str, None] = "15f5f15641e8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("idx_game_stats_level_class"), table_name="character_game_stats")
    op.drop_index(op.f("ix_character_game_stats_character_id"), table_name="character_game_stats")
    op.create_unique_constraint(None, "character_game_stats", ["character_id"])
    op.drop_column("character_game_stats", "hit_dice")
    op.drop_column("character_game_stats", "weapon_proficiencies")
    op.drop_column("character_game_stats", "spellcasting_ability")
    op.drop_column("character_game_stats", "proficiency_bonus")
    op.drop_column("character_game_stats", "armor_proficiencies")
    op.drop_column("character_game_stats", "character_class")
    op.drop_column("character_game_stats", "spell_save_dc")
    op.drop_column("character_game_stats", "spell_attack_bonus")
    op.drop_column("character_game_stats", "tool_proficiencies")
    op.drop_column("character_game_stats", "spell_slots")
    op.drop_column("character_game_stats", "languages")
    op.drop_column("character_game_stats", "proficient_skills")
    op.drop_column("character_game_stats", "spells_known")
    op.drop_column("character_game_stats", "character_subclass")
    op.drop_column("character_game_stats", "background")
    op.drop_column("character_game_stats", "alignment")
    op.drop_column("character_game_stats", "proficient_saves")
    op.drop_column("characters", "personality_traits")
    op.drop_index(op.f("idx_faction_hierarchy"), table_name="factions")
    op.drop_index(op.f("ix_factions_parent_faction_id"), table_name="factions")
    op.drop_constraint(op.f("factions_parent_faction_id_fkey"), "factions", type_="foreignkey")
    op.drop_column("factions", "parent_faction_id")
    op.drop_index(op.f("idx_location_type_region"), table_name="locations")
    op.drop_index(op.f("ix_locations_type"), table_name="locations")
    op.drop_column("locations", "type")
    op.drop_index(op.f("ix_races_rarity"), table_name="races")
    op.drop_column("races", "special_traits")
    op.drop_column("races", "rarity")
    op.drop_index(op.f("idx_users_2fa_enabled"), table_name="users")
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f("idx_users_2fa_enabled"), "users", ["is_2fa_enabled"], unique=False)
    op.add_column(
        "races",
        sa.Column("rarity", sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    )
    op.add_column(
        "races",
        sa.Column("special_traits", sa.TEXT(), autoincrement=False, nullable=True),
    )
    op.create_index(op.f("ix_races_rarity"), "races", ["rarity"], unique=False)
    op.add_column(
        "locations",
        sa.Column("type", sa.VARCHAR(length=30), autoincrement=False, nullable=False),
    )
    op.create_index(op.f("ix_locations_type"), "locations", ["type"], unique=False)
    op.create_index(op.f("idx_location_type_region"), "locations", ["type", "region"], unique=False)
    op.add_column(
        "factions",
        sa.Column("parent_faction_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.create_foreign_key(
        op.f("factions_parent_faction_id_fkey"),
        "factions",
        "factions",
        ["parent_faction_id"],
        ["id"],
    )
    op.create_index(
        op.f("ix_factions_parent_faction_id"),
        "factions",
        ["parent_faction_id"],
        unique=False,
    )
    op.create_index(
        op.f("idx_faction_hierarchy"),
        "factions",
        ["parent_faction_id", "type"],
        unique=False,
    )
    op.add_column(
        "characters",
        sa.Column("personality_traits", sa.TEXT(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "character_game_stats",
        sa.Column(
            "proficient_saves",
            postgresql.ARRAY(sa.VARCHAR()),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "character_game_stats",
        sa.Column("alignment", sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    )
    op.add_column(
        "character_game_stats",
        sa.Column("background", sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    )
    op.add_column(
        "character_game_stats",
        sa.Column(
            "character_subclass",
            sa.VARCHAR(length=50),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "character_game_stats",
        sa.Column(
            "spells_known",
            postgresql.ARRAY(sa.VARCHAR()),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "character_game_stats",
        sa.Column(
            "proficient_skills",
            postgresql.ARRAY(sa.VARCHAR()),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "character_game_stats",
        sa.Column(
            "languages",
            postgresql.ARRAY(sa.VARCHAR()),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "character_game_stats",
        sa.Column(
            "spell_slots",
            postgresql.JSONB(astext_type=sa.Text()),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "character_game_stats",
        sa.Column(
            "tool_proficiencies",
            postgresql.ARRAY(sa.VARCHAR()),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "character_game_stats",
        sa.Column("spell_attack_bonus", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "character_game_stats",
        sa.Column("spell_save_dc", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "character_game_stats",
        sa.Column("character_class", sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    )
    op.add_column(
        "character_game_stats",
        sa.Column(
            "armor_proficiencies",
            postgresql.ARRAY(sa.VARCHAR()),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "character_game_stats",
        sa.Column("proficiency_bonus", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "character_game_stats",
        sa.Column(
            "spellcasting_ability",
            sa.VARCHAR(length=20),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "character_game_stats",
        sa.Column(
            "weapon_proficiencies",
            postgresql.ARRAY(sa.VARCHAR()),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "character_game_stats",
        sa.Column("hit_dice", sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    )
    op.drop_constraint(None, "character_game_stats", type_="unique")
    op.create_index(
        op.f("ix_character_game_stats_character_id"),
        "character_game_stats",
        ["character_id"],
        unique=True,
    )
    op.create_index(
        op.f("idx_game_stats_level_class"),
        "character_game_stats",
        ["level", "character_class"],
        unique=False,
    )
    # ### end Alembic commands ###
