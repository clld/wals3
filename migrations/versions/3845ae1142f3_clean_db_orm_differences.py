# coding=utf-8
"""clean db orm differences

Revision ID: 3845ae1142f3
Revises: 1f1b73a8171
Create Date: 2015-04-27 16:57:04.955000

"""

# revision identifiers, used by Alembic.
revision = '3845ae1142f3'
down_revision = '1f1b73a8171'

import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_table('unitparameterunit')
    op.drop_table('unitparameterunit_history')
    op.drop_column('feature', 'id')
    op.drop_column('feature_history', 'id')


def downgrade():
    pass
