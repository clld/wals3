# coding=ascii
"""add chapter s2

Revision ID: 
Revises: 
Create Date: 

"""
from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = ''
down_revision = ''

import datetime

from alembic import op
import sqlalchemy as sa


ID, NAME, SORTKEY = 's2', 'List of abbreviations', 992

def upgrade():
    conn = op.get_bind()

    cocols = [
        'created', 'updated', 'active', 'version', 'polymorphic_type',
        'id', 'name',
    ]
    co = sa.table('contribution', *map(sa.column, ['pk'] + cocols))
    chcols = ['pk', 'sortkey']
    ch = sa.table('chapter', *map(sa.column, chcols))

    id_, name = map(sa.bindparam, ['id_', 'name'])

    cowhere = [co.c.id == id_, co.c.name == name]

    insert_co = co.insert(bind=conn).from_select(cocols,
        sa.select([sa.func.now(), sa.func.now(), True, 1, sa.literal('custom'), id_, name])
        .where(~sa.exists().where(sa.or_(*cowhere))))

    co_pk = sa.select([co.c.pk]).where(sa.and_(*cowhere)).as_scalar()
    sortkey = sa.bindparam('sortkey')

    insert_ch = ch.insert(bind=conn).from_select(chcols,
        sa.select([co_pk, sortkey])
        .where(~sa.exists().where(ch.c.pk == co.c.pk).where(sa.or_(*cowhere)))
        .where(sa.exists().where(sa.and_(*cowhere))))

    insert_co.execute(id_=ID, name=NAME)
    insert_ch.execute(id_=ID, name=NAME, sortkey=SORTKEY)

    raise NotImplementedError


def downgrade():
    pass
