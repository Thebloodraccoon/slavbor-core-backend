"""Add admin

Revision ID: d0b85052499a
Revises: 3c77983469e3
Create Date: 2025-06-11 06:54:03.764939

"""

from datetime import datetime, timezone
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import text

from app.settings import settings
from app.utils.auth import get_password_hash

# revision identifiers, used by Alembic.
revision: str = "d0b85052499a"
down_revision: Union[str, None] = "3c77983469e3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_EMAIL = settings.ADMIN_LOGIN
DEFAULT_ADMIN_PASSWORD = settings.ADMIN_PASSWORD

users_table = sa.table(
    "users",
    sa.column("id", sa.Integer),
    sa.column("username", sa.String),
    sa.column("email", sa.String),
    sa.column("hashed_password", sa.String),
    sa.column("role", sa.String),
    sa.column("created_at", sa.DateTime),
    sa.column("updated_at", sa.DateTime),
    sa.column("last_login", sa.DateTime),
)


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()

    stmt = sa.text("SELECT id FROM users WHERE email = :email")
    admin_exists = (
        conn.execute(stmt, {"email": DEFAULT_ADMIN_EMAIL}).fetchone() is not None
    )

    if admin_exists:
        stmt = sa.text(
            """
            UPDATE users 
            SET hashed_password = :hashed_password,
                updated_at = :updated_at
            WHERE email = :email
        """
        )

        conn.execute(
            stmt,
            {
                "email": DEFAULT_ADMIN_EMAIL,
                "hashed_password": get_password_hash(DEFAULT_ADMIN_PASSWORD),
                "updated_at": datetime.now(timezone.utc),
            },
        )
    else:
        op.bulk_insert(
            users_table,
            [
                {
                    "username": DEFAULT_ADMIN_USERNAME,
                    "email": DEFAULT_ADMIN_EMAIL,
                    "hashed_password": get_password_hash(DEFAULT_ADMIN_PASSWORD),
                    "role": "found_father",
                    "created_at": datetime.now(timezone.utc),
                    "updated_at": datetime.now(timezone.utc),
                    "last_login": None,
                }
            ],
        )


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    stmt = sa.text("DELETE FROM users WHERE email = :email")
    conn.execute(stmt, {"email": DEFAULT_ADMIN_EMAIL})
