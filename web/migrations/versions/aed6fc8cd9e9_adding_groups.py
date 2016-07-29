"""adding groups

Revision ID: aed6fc8cd9e9
Revises: 636e6665f57f
Create Date: 2016-07-24 00:31:02.253762

"""

# revision identifiers, used by Alembic.
revision = 'aed6fc8cd9e9'
down_revision = '636e6665f57f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.VARCHAR(255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    )

    op.create_table('group_members',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='CASCADE', ondelete='CASCADE'),
    )

def downgrade():
    op.drop_table('groups')
    op.drop_table('group_members')
