"""non nullable user columns

Revision ID: d9686ec79bef
Revises: 3b325b031408
Create Date: 2016-04-19 21:58:48.077736

"""

# revision identifiers, used by Alembic.
revision = 'd9686ec79bef'
down_revision = '3b325b031408'

from alembic import op
import sqlalchemy as sa


def upgrade():
	op.alter_column('users', 'id', autoincrement=True, existing_type=sa.INT)
	op.alter_column('users', 'mobile_number', nullable=False, existing_type=sa.VARCHAR(255))

def downgrade():
	op.alter_column('users', 'id', autoincrement=False, existing_type=sa.INT)
	op.alter_column('users', 'mobile_number', nullable=True, existing_type=sa.VARCHAR(255))
