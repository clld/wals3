# coding=utf-8
"""rename hnk

Revision ID: 1f1b73a8171
Revises: d0781108893
Create Date: 2015-03-17 12:29:36.184000

"""

# revision identifiers, used by Alembic.
revision = '1f1b73a8171'
down_revision = 'd0781108893'

import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute(sa.text('UPDATE language SET updated = now(), '
        'name = :after WHERE id = :id AND name = :before'
        ).bindparams(id='hnk', before='Hinukh', after='Hinuq'))


def downgrade():
    pass
