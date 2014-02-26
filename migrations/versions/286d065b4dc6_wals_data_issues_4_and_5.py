# coding=utf-8
"""wals-data issues 4 and 5

Revision ID: 286d065b4dc6
Revises: 1e748a54b964
Create Date: 2014-02-26 20:12:16.091367

"""
from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '286d065b4dc6'
down_revision = '1e748a54b964'

import datetime

from alembic import op
import sqlalchemy as sa

from clld.db.migration import Connection
from clld.db.models.common import Language

from wals3.models import WalsLanguage


def upgrade():
    conn = Connection(op.get_bind())

    # The language Nishi, with WALS code nis should be renamed Nyishi.
    pk = conn.pk(Language, 'nis')
    conn.update(Language, [('name', 'Nyishi')], pk=pk)
    conn.update(WalsLanguage, [('ascii_name', 'nyishi')], pk=pk)

    # Munzumbo [mnz] should be Munzombo
    pk = conn.pk(Language, 'mnz')
    conn.update(Language, [('name', 'Munzombo')], pk=pk)
    conn.update(WalsLanguage, [('ascii_name', 'munzombo')], pk=pk)


def downgrade():
    pass
