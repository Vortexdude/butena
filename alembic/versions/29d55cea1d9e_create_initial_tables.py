"""create initial tables

Revision ID: 29d55cea1d9e
Revises: 
Create Date: 2024-03-05 15:06:42.298946

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '29d55cea1d9e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('deployments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=256), nullable=False),
    sa.Column('bucket', sa.String(length=40), nullable=False),
    sa.Column('zone', sa.String(length=15), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('user_account',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=256), nullable=False),
    sa.Column('email', sa.String(length=30), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('user_name', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(length=256), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_account')
    op.drop_table('deployments')
    # ### end Alembic commands ###
