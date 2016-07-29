"""Add user table

Revision ID: 4611a01ff949
Revises: None
Create Date: 2016-04-03 23:30:12.742732

"""

# revision identifiers, used by Alembic.
revision = '4611a01ff949'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.VARCHAR(255), nullable=True),
    sa.Column('phonenumber', sa.VARCHAR(255), nullable=False),
    sa.Column('email', sa.VARCHAR(255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    pass

def downgrade():
    pass
