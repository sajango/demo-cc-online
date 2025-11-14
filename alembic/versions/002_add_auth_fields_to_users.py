"""add auth fields to users

Revision ID: 002
Revises: 001
Create Date: 2025-11-14

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add authentication fields to users table"""
    # Add password_hash column (nullable for OAuth users)
    op.add_column('users', sa.Column('password_hash', sa.String(255), nullable=True))

    # Add auth_provider column with default 'local'
    op.add_column('users', sa.Column(
        'auth_provider',
        sa.Enum('local', 'google', 'apple', name='authprovider'),
        nullable=False,
        server_default='local'
    ))

    # Add oauth_provider_id column (nullable, indexed)
    op.add_column('users', sa.Column('oauth_provider_id', sa.String(255), nullable=True))
    op.create_index('ix_users_oauth_provider_id', 'users', ['oauth_provider_id'])

    # Add is_verified column with default False
    op.add_column('users', sa.Column('is_verified', sa.Boolean(), nullable=False, server_default='0'))


def downgrade() -> None:
    """Remove authentication fields from users table"""
    op.drop_index('ix_users_oauth_provider_id', 'users')
    op.drop_column('users', 'is_verified')
    op.drop_column('users', 'oauth_provider_id')
    op.drop_column('users', 'auth_provider')
    op.drop_column('users', 'password_hash')
