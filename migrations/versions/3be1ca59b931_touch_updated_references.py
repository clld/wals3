# coding=ascii
"""touch updated references

Revision ID: 3be1ca59b931
Revises: eb2efcd10cf
Create Date: 2017-10-19 14:16:12.345000

"""
from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '3be1ca59b931'
down_revision = u'eb2efcd10cf'

import datetime

from alembic import op
import sqlalchemy as sa

# cf. 351dc2c86238dae5cfe85c3faa4dcc3e2bd7a651 (183a783fc885_fix_references.py)

IDS = [
    'Arnasonar-1980',
    'Buenrostros-1991',
    'Muller-1858',
    'Camargo-Bigot-1992',
    'Kuzmenkov-et-al-2007',
]

UPDATED = datetime.datetime(2017, 10, 18, 17, 00)


def upgrade():
    source = sa.table('source', sa.column('id'), sa.column('updated', sa.DateTime))
    dt = sa.bindparam('dt', UPDATED)
    touch = sa.update(source, bind=op.get_bind())\
        .where(source.c.id == sa.bindparam('id_'))\
        .where(source.c.updated < dt)\
        .values(updated=dt)

    for id_ in IDS:
        touch.execute(id_=id_)


def downgrade():
    pass
