"""Adding password field

Revision ID: 7fb980ed1cdd
Revises: aed6fc8cd9e9
Create Date: 2016-07-26 22:03:23.000174

"""

# revision identifiers, used by Alembic.
revision = '7fb980ed1cdd'
down_revision = 'aed6fc8cd9e9'

from alembic import op
import sqlalchemy as sa


def upgrade():
	op.add_column('users', sa.Column('password', sa.String(255), nullable=True))
	op.add_column('users', sa.Column('date_confirmed', sa.DateTime(), nullable=True))

def downgrade():
	op.drop_column('users', 'password')
	op.drop_column('users', 'date_confirmed')
