"""Add 2fa fields to user

Revision ID: 15f5f15641e8
Revises: 9f03f1e703a4
Create Date: 2025-07-03 08:39:50.426591

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "15f5f15641e8"
down_revision: Union[str, None] = "9f03f1e703a4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add other fields first
    op.add_column("users", sa.Column("phone", sa.String(length=20), nullable=True))
    op.add_column("users", sa.Column("bio", sa.Text(), nullable=True))
    op.add_column("users", sa.Column("otp_secret", sa.String(), nullable=True))

    # Add is_2fa_enabled as nullable first
    op.add_column("users", sa.Column("is_2fa_enabled", sa.Boolean(), nullable=True))

    # Set default value for existing records
    op.execute("UPDATE users SET is_2fa_enabled = false WHERE is_2fa_enabled IS NULL")

    # Now make it NOT NULL
    op.alter_column("users", "is_2fa_enabled", nullable=False)

    # Add index for performance
    op.create_index("idx_users_2fa_enabled", "users", ["is_2fa_enabled"])


def downgrade() -> None:
    """Downgrade schema."""
    # Drop index first
    op.drop_index("idx_users_2fa_enabled", "users")

    # Drop columns
    op.drop_column("users", "otp_secret")
    op.drop_column("users", "is_2fa_enabled")
    op.drop_column("users", "bio")
    op.drop_column("users", "phone")
