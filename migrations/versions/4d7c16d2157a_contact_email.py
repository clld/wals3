# coding=utf-8
"""contact email

Revision ID: 4d7c16d2157a
Revises: 4417c4a41762
Create Date: 2015-10-07 10:49:31.606056

"""

# revision identifiers, used by Alembic.
revision = '4d7c16d2157a'
down_revision = '4417c4a41762'

import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute("UPDATE dataset SET contact = 'wals@shh.mpg.de'")


def downgrade():
    pass
