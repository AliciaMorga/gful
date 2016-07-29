"""rename phonenumber column

Revision ID: 3b325b031408
Revises: 4611a01ff949
Create Date: 2016-04-13 20:46:40.628868

"""

# revision identifiers, used by Alembic.
revision = '3b325b031408'
down_revision = '4611a01ff949'

from alembic import op
import sqlalchemy as sa

def upgrade():
	op.alter_column('users', 'phonenumber', existing_type=sa.VARCHAR(255), new_column_name='mobile_number')

def downgrade():
	op.alter_column('users', 'mobile_number', existing_type=sa.VARCHAR(255), new_column_name='phonenumber')