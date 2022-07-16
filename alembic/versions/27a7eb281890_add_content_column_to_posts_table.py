"""add content column to posts table

Revision ID: 27a7eb281890
Revises: b2e07e448042
Create Date: 2022-07-14 19:56:53.054071

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27a7eb281890'
down_revision = 'b2e07e448042'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
