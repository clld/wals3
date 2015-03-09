# coding=utf-8
"""rename pnu

Revision ID: d0781108893
Revises: 53a5f6f0a2ef
Create Date: 2015-03-09 10:39:11.561000

"""

# revision identifiers, used by Alembic.
revision = 'd0781108893'
down_revision = '53a5f6f0a2ef'

import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute(sa.text('UPDATE language SET updated = now(), '
        'name = :after WHERE id = :id AND name = :before'
        ).bindparams(id='pnu', before='Punu', after='Bunu (Younuo)'))


def downgrade():
    pass
