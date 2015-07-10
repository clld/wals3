# coding=utf-8
"""correct Frantz 1973

Revision ID: 342705ff1484
Revises: 108c6a424057
Create Date: 2015-07-10 10:21:27.630370

"""
from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '342705ff1484'
down_revision = u'108c6a424057'

import datetime

from alembic import op
import sqlalchemy as sa

from clld.db.migration import Connection
from clld.db.models.common import Source


def upgrade():
    conn = Connection(op.get_bind())
    conn.update(Source, [('pages', '424-438')], id='Frantz-1973')


def downgrade():
    pass
