"""create-users

Revision ID: 550fdfa00ae9
Revises:
Create Date: 2025-03-04 15:21:06.745244
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '550fdfa00ae9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'users',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('username', sa.String(length=20), nullable=False),
        sa.Column('password', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=20), nullable=False),
        sa.Column('last_name', sa.String(length=80), nullable=False),
        sa.Column('email', sa.String(length=50), nullable=False),
        sa.Column('phone', sa.String(length=50), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
