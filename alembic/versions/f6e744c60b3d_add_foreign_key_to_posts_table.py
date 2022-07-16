"""add foreign-key to posts table

Revision ID: f6e744c60b3d
Revises: 1ad26650c5f1
Create Date: 2022-07-15 09:02:46.400646

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6e744c60b3d'
down_revision = '1ad26650c5f1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))  
    op.create_foreign_key('posts_users_fk', source_table="posts", 
                                           referent_table="users", 
                                           local_cols=['user_id'], 
                                           remote_cols=['id'],
                                           ondelete="CASCADE")
    pass    

    # ova funkcija dodaje novu kolonu "user_id" u tabelu "posts" koja je foreign key 
    # remote_cols je kolona iz "users tabele"  


def downgrade():
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'user_id')
    pass
