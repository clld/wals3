# coding=utf-8
"""macro-ge classification

https://github.com/clld/wals-data/issues/62

Revision ID: 4e5cdd2c9cfe
Revises: 13b08c8d306b
Create Date: 2015-10-09 13:22:01.566539

"""
from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '4e5cdd2c9cfe'
down_revision = u'13b08c8d306b'

import datetime

from alembic import op
import sqlalchemy as sa

from wals3.migration import Connection
from wals3.models import Family, Genus


FAMILIES = {
    'guato': ('guato', 'Guató'),
    'yate': ('yate', 'Yatê'),
    'bororo': ('bororoan', 'Bororoan'),
}


def upgrade():
    conn = Connection(op.get_bind())

    # https://github.com/clld/wals-data/issues/62
    for gid, (fid, fname) in FAMILIES.items():
        fpk = conn.insert(Family, id=fid, name=fname)
        conn.update(Genus, dict(family_pk=fpk), id=gid)

    conn.update(Genus, dict(name='Bororoan'), id='bororo')


def downgrade():
    pass
