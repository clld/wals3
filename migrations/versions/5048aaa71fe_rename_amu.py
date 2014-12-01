# coding=utf-8
"""rename amu

Revision ID: 5048aaa71fe
Revises: 72e9e0c0473
Create Date: 2014-12-01 14:21:13.643000

"""

# revision identifiers, used by Alembic.
revision = '5048aaa71fe'
down_revision = '72e9e0c0473'

import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute(sa.text('UPDATE language SET updated = now(), '
        'name = :after WHERE id = :id AND name = :before'
        ).bindparams(id='amu', before='Amuesha', after="Yanesha'"))


def downgrade():
    pass
