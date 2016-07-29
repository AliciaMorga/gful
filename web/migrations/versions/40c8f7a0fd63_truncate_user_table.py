"""truncate user table

Revision ID: 40c8f7a0fd63
Revises: d9686ec79bef
Create Date: 2016-04-19 22:15:18.896154

"""

# revision identifiers, used by Alembic.
revision = '40c8f7a0fd63'
down_revision = 'd9686ec79bef'

from alembic import op
import sqlalchemy as sa


def upgrade():
	op.drop_table('users')
	op.create_table('users',
	sa.Column('id', sa.Integer(), nullable=False),
	sa.Column('name', sa.VARCHAR(255), nullable=True),
	sa.Column('mobile_number', sa.VARCHAR(255), nullable=False),
	sa.Column('email', sa.VARCHAR(255), nullable=True),
	sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    pass
