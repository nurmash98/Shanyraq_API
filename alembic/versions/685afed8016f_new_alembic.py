"""new alembic

Revision ID: 685afed8016f
Revises: 
Create Date: 2023-07-28 23:54:59.278205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '685afed8016f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_index(op.f('ix_users_user_id'), 'users', ['user_id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)
    op.create_table('announcements',
    sa.Column('announce_id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('area', sa.Integer(), nullable=True),
    sa.Column('rooms_count', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('announce_id')
    )
    op.create_index(op.f('ix_announcements_announce_id'), 'announcements', ['announce_id'], unique=False)
    op.create_index(op.f('ix_announcements_type'), 'announcements', ['type'], unique=False)
    op.create_table('comments',
    sa.Column('comment_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('announce_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['announce_id'], ['announcements.announce_id'], ),
    sa.ForeignKeyConstraint(['author_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('comment_id')
    )
    op.create_index(op.f('ix_comments_comment_id'), 'comments', ['comment_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_comments_comment_id'), table_name='comments')
    op.drop_table('comments')
    op.drop_index(op.f('ix_announcements_type'), table_name='announcements')
    op.drop_index(op.f('ix_announcements_announce_id'), table_name='announcements')
    op.drop_table('announcements')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_user_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###